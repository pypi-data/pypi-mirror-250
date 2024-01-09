"""Everything related to fetching or initializing build prerequisites."""

from __future__ import annotations

import glob
import importlib
import json
import os
import platform
import random
import re
import stat
import sys
import tempfile
import zipfile
from fileinput import FileInput
from pathlib import Path
from types import ModuleType

import httpx
import pkg_resources
import typer
from alembic.util.exc import CommandError
from packaging import version
from redis.asyncio import Redis

from reflex import constants, model
from reflex.compiler import templates
from reflex.config import get_config
from reflex.utils import console, path_ops, processes


def check_latest_package_version(package_name: str):
    """Check if the latest version of the package is installed.

    Args:
        package_name: The name of the package.
    """
    try:
        # Get the latest version from PyPI
        current_version = pkg_resources.get_distribution(package_name).version
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = httpx.get(url)
        latest_version = response.json()["info"]["version"]
        if version.parse(current_version) < version.parse(latest_version):
            console.warn(
                f"Your version ({current_version}) of {package_name} is out of date. Upgrade to {latest_version} with 'pip install {package_name} --upgrade'"
            )
    except Exception:
        pass


def check_node_version() -> bool:
    """Check the version of Node.js.

    Returns:
        Whether the version of Node.js is valid.
    """
    current_version = get_node_version()
    if current_version:
        # Compare the version numbers
        return (
            current_version >= version.parse(constants.Node.MIN_VERSION)
            if constants.IS_WINDOWS
            else current_version == version.parse(constants.Node.VERSION)
        )
    return False


def get_node_version() -> version.Version | None:
    """Get the version of node.

    Returns:
        The version of node.
    """
    try:
        result = processes.new_process([path_ops.get_node_path(), "-v"], run=True)
        # The output will be in the form "vX.Y.Z", but version.parse() can handle it
        return version.parse(result.stdout)  # type: ignore
    except (FileNotFoundError, TypeError):
        return None


def get_fnm_version() -> version.Version | None:
    """Get the version of fnm.

    Returns:
        The version of FNM.
    """
    try:
        result = processes.new_process([constants.Fnm.EXE, "--version"], run=True)
        return version.parse(result.stdout.split(" ")[1])  # type: ignore
    except (FileNotFoundError, TypeError):
        return None


def get_bun_version() -> version.Version | None:
    """Get the version of bun.

    Returns:
        The version of bun.
    """
    try:
        # Run the bun -v command and capture the output
        result = processes.new_process([get_config().bun_path, "-v"], run=True)
        return version.parse(result.stdout)  # type: ignore
    except FileNotFoundError:
        return None


def get_install_package_manager() -> str | None:
    """Get the package manager executable for installation.
      Currently on unix systems, bun is used for installation only.

    Returns:
        The path to the package manager.
    """
    # On Windows, we use npm instead of bun.
    if constants.IS_WINDOWS:
        return get_package_manager()

    # On other platforms, we use bun.
    return get_config().bun_path


def get_package_manager() -> str | None:
    """Get the package manager executable for running app.
      Currently on unix systems, npm is used for running the app only.

    Returns:
        The path to the package manager.
    """
    npm_path = path_ops.get_npm_path()
    if npm_path is not None:
        npm_path = str(Path(npm_path).resolve())
    return npm_path


def get_app(reload: bool = False) -> ModuleType:
    """Get the app module based on the default config.

    Args:
        reload: Re-import the app module from disk

    Returns:
        The app based on the default config.

    Raises:
        RuntimeError: If the app name is not set in the config.
    """
    os.environ[constants.RELOAD_CONFIG] = str(reload)
    config = get_config()
    if not config.app_name:
        raise RuntimeError(
            "Cannot get the app module because `app_name` is not set in rxconfig! "
            "If this error occurs in a reflex test case, ensure that `get_app` is mocked."
        )
    module = ".".join([config.app_name, config.app_name])
    sys.path.insert(0, os.getcwd())
    app = __import__(module, fromlist=(constants.CompileVars.APP,))
    if reload:
        from reflex.state import State

        # Reset rx.State subclasses to avoid conflict when reloading.
        State.class_subclasses.clear()
        # Reload the app module.
        importlib.reload(app)

    return app


def get_compiled_app(reload: bool = False) -> ModuleType:
    """Get the app module based on the default config after first compiling it.

    Args:
        reload: Re-import the app module from disk

    Returns:
        The compiled app based on the default config.
    """
    app_module = get_app(reload=reload)
    getattr(app_module, constants.CompileVars.APP).compile_()
    return app_module


def get_redis() -> Redis | None:
    """Get the redis client.

    Returns:
        The redis client.
    """
    config = get_config()
    if not config.redis_url:
        return None
    if config.redis_url.startswith(("redis://", "rediss://", "unix://")):
        return Redis.from_url(config.redis_url)
    console.deprecate(
        feature_name="host[:port] style redis urls",
        reason="redis-py url syntax is now being used",
        deprecation_version="0.3.6",
        removal_version="0.4.0",
    )
    redis_url, has_port, redis_port = config.redis_url.partition(":")
    if not has_port:
        redis_port = 6379
    console.info(f"Using redis at {config.redis_url}")
    return Redis(host=redis_url, port=int(redis_port), db=0)


def get_production_backend_url() -> str:
    """Get the production backend URL.

    Returns:
        The production backend URL.
    """
    config = get_config()
    return constants.PRODUCTION_BACKEND_URL.format(
        username=config.username,
        app_name=config.app_name,
    )


def validate_app_name(app_name: str | None = None) -> str:
    """Validate the app name.

    The default app name is the name of the current directory.

    Args:
        app_name: the name passed by user during reflex init

    Returns:
        The app name after validation.

    Raises:
        Exit: if the app directory name is reflex or if the name is not standard for a python package name.
    """
    app_name = (
        app_name if app_name else os.getcwd().split(os.path.sep)[-1].replace("-", "_")
    )
    # Make sure the app is not named "reflex".
    if app_name == constants.Reflex.MODULE_NAME:
        console.error(
            f"The app directory cannot be named [bold]{constants.Reflex.MODULE_NAME}[/bold]."
        )
        raise typer.Exit(1)

    # Make sure the app name is standard for a python package name.
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", app_name):
        console.error(
            "The app directory name must start with a letter and can contain letters, numbers, and underscores."
        )
        raise typer.Exit(1)

    return app_name


def create_config(app_name: str):
    """Create a new rxconfig file.

    Args:
        app_name: The name of the app.
    """
    # Import here to avoid circular imports.
    from reflex.compiler import templates

    config_name = f"{re.sub(r'[^a-zA-Z]', '', app_name).capitalize()}Config"
    with open(constants.Config.FILE, "w") as f:
        console.debug(f"Creating {constants.Config.FILE}")
        f.write(templates.RXCONFIG.render(app_name=app_name, config_name=config_name))


def initialize_gitignore():
    """Initialize the template .gitignore file."""
    # The files to add to the .gitignore file.
    files = constants.GitIgnore.DEFAULTS

    # Subtract current ignored files.
    if os.path.exists(constants.GitIgnore.FILE):
        with open(constants.GitIgnore.FILE, "r") as f:
            files |= set([line.strip() for line in f.readlines()])

    # Write files to the .gitignore file.
    with open(constants.GitIgnore.FILE, "w") as f:
        console.debug(f"Creating {constants.GitIgnore.FILE}")
        f.write(f"{(path_ops.join(sorted(files))).lstrip()}")


def initialize_requirements_txt():
    """Initialize the requirements.txt file.
    If absent, generate one for the user.
    If the requirements.txt does not have reflex as dependency,
    generate a requirement pinning current version and append to
    the requirements.txt file.
    """
    fp = Path(constants.RequirementsTxt.FILE)
    encoding = "utf-8"
    if not fp.exists():
        fp.touch()
    else:
        # Detect the encoding of the original file
        import charset_normalizer

        charset_matches = charset_normalizer.from_path(fp)
        maybe_charset_match = charset_matches.best()
        if maybe_charset_match is None:
            console.debug(f"Unable to detect encoding for {fp}, exiting.")
            return
        encoding = maybe_charset_match.encoding
        console.debug(f"Detected encoding for {fp} as {encoding}.")
    try:
        other_requirements_exist = False
        with open(fp, "r", encoding=encoding) as f:
            for req in f.readlines():
                # Check if we have a package name that is reflex
                if re.match(r"^reflex[^a-zA-Z0-9]", req):
                    console.debug(f"{fp} already has reflex as dependency.")
                    return
                other_requirements_exist = True
        with open(fp, "a", encoding=encoding) as f:
            preceding_newline = "\n" if other_requirements_exist else ""
            f.write(
                f"{preceding_newline}{constants.RequirementsTxt.DEFAULTS_STUB}{constants.Reflex.VERSION}\n"
            )
    except Exception:
        console.info(f"Unable to check {fp} for reflex dependency.")


def initialize_app_directory(app_name: str, template: constants.Templates.Kind):
    """Initialize the app directory on reflex init.

    Args:
        app_name: The name of the app.
        template: The template to use.
    """
    console.log("Initializing the app directory.")

    # Copy the template to the current directory.
    template_dir = Path(constants.Templates.Dirs.BASE, "apps", template.value)

    # Remove all pyc and __pycache__ dirs in template directory.
    for pyc_file in template_dir.glob("**/*.pyc"):
        pyc_file.unlink()
    for pycache_dir in template_dir.glob("**/__pycache__"):
        pycache_dir.rmdir()

    for file in template_dir.iterdir():
        # Copy the file to current directory but keep the name the same.
        path_ops.cp(str(file), file.name)

    # Rename the template app to the app name.
    path_ops.mv(constants.Templates.Dirs.CODE, app_name)
    path_ops.mv(
        os.path.join(app_name, template_dir.name + constants.Ext.PY),
        os.path.join(app_name, app_name + constants.Ext.PY),
    )

    # Fix up the imports.
    path_ops.find_replace(
        app_name,
        f"from {constants.Templates.Dirs.CODE}",
        f"from {app_name}",
    )


def get_project_hash() -> int | None:
    """Get the project hash from the reflex.json file if the file exists.

    Returns:
        project_hash: The app hash.
    """
    if not os.path.exists(constants.Reflex.JSON):
        return None
    # Open and read the file
    with open(constants.Reflex.JSON, "r") as file:
        data = json.load(file)
        project_hash = data["project_hash"]
        return project_hash


def initialize_web_directory():
    """Initialize the web directory on reflex init."""
    console.log("Initializing the web directory.")

    # Re-use the hash if one is already created, so we don't over-write it when running reflex init
    project_hash = get_project_hash()

    path_ops.cp(constants.Templates.Dirs.WEB_TEMPLATE, constants.Dirs.WEB)

    initialize_package_json()

    path_ops.mkdir(constants.Dirs.WEB_ASSETS)

    update_next_config()

    # Initialize the reflex json file.
    init_reflex_json(project_hash=project_hash)


def _compile_package_json():
    return templates.PACKAGE_JSON.render(
        scripts={
            "dev": constants.PackageJson.Commands.DEV,
            "export": constants.PackageJson.Commands.EXPORT,
            "export_sitemap": constants.PackageJson.Commands.EXPORT_SITEMAP,
            "prod": constants.PackageJson.Commands.PROD,
        },
        dependencies=constants.PackageJson.DEPENDENCIES,
        dev_dependencies=constants.PackageJson.DEV_DEPENDENCIES,
    )


def initialize_package_json():
    """Render and write in .web the package.json file."""
    output_path = constants.PackageJson.PATH
    code = _compile_package_json()
    with open(output_path, "w") as file:
        file.write(code)


def init_reflex_json(project_hash: int | None):
    """Write the hash of the Reflex project to a REFLEX_JSON.

    Re-use the hash if one is already created, therefore do not
    overwrite it every time we run the reflex init command
    .

    Args:
        project_hash: The app hash.
    """
    if project_hash is not None:
        console.debug(f"Project hash is already set to {project_hash}.")
    else:
        # Get a random project hash.
        project_hash = random.getrandbits(128)
        console.debug(f"Setting project hash to {project_hash}.")

    # Write the hash and version to the reflex json file.
    reflex_json = {
        "version": constants.Reflex.VERSION,
        "project_hash": project_hash,
    }
    path_ops.update_json_file(constants.Reflex.JSON, reflex_json)


def update_next_config(export=False):
    """Update Next.js config from Reflex config.

    Args:
        export: if the method run during reflex export.
    """
    next_config_file = os.path.join(constants.Dirs.WEB, constants.Next.CONFIG_FILE)

    next_config = _update_next_config(get_config(), export=export)

    with open(next_config_file, "w") as file:
        file.write(next_config)
        file.write("\n")


def _update_next_config(config, export=False):
    next_config = {
        "basePath": config.frontend_path or "",
        "compress": config.next_compression,
        "reactStrictMode": True,
        "trailingSlash": True,
    }
    if export:
        next_config["output"] = "export"
        next_config["distDir"] = constants.Dirs.STATIC

    next_config_json = re.sub(r'"([^"]+)"(?=:)', r"\1", json.dumps(next_config))
    return f"module.exports = {next_config_json};"


def remove_existing_bun_installation():
    """Remove existing bun installation."""
    console.debug("Removing existing bun installation.")
    if os.path.exists(get_config().bun_path):
        path_ops.rm(constants.Bun.ROOT_PATH)


def download_and_run(url: str, *args, show_status: bool = False, **env):
    """Download and run a script.

    Args:
        url: The url of the script.
        args: The arguments to pass to the script.
        show_status: Whether to show the status of the script.
        env: The environment variables to use.
    """
    # Download the script
    console.debug(f"Downloading {url}")
    response = httpx.get(url)
    if response.status_code != httpx.codes.OK:
        response.raise_for_status()

    # Save the script to a temporary file.
    script = tempfile.NamedTemporaryFile()
    with open(script.name, "w") as f:
        f.write(response.text)

    # Run the script.
    env = {**os.environ, **env}
    process = processes.new_process(["bash", f.name, *args], env=env)
    show = processes.show_status if show_status else processes.show_logs
    show(f"Installing {url}", process)


def download_and_extract_fnm_zip():
    """Download and run a script.

    Raises:
        Exit: If an error occurs while downloading or extracting the FNM zip.
    """
    # Download the zip file
    url = constants.Fnm.INSTALL_URL
    console.debug(f"Downloading {url}")
    fnm_zip_file = os.path.join(constants.Fnm.DIR, f"{constants.Fnm.FILENAME}.zip")
    # Function to download and extract the FNM zip release.
    try:
        # Download the FNM zip release.
        # TODO: show progress to improve UX
        with httpx.stream("GET", url, follow_redirects=True) as response:
            response.raise_for_status()
            with open(fnm_zip_file, "wb") as output_file:
                for chunk in response.iter_bytes():
                    output_file.write(chunk)

        # Extract the downloaded zip file.
        with zipfile.ZipFile(fnm_zip_file, "r") as zip_ref:
            zip_ref.extractall(constants.Fnm.DIR)

        console.debug("FNM package downloaded and extracted successfully.")
    except Exception as e:
        console.error(f"An error occurred while downloading fnm package: {e}")
        raise typer.Exit(1) from e
    finally:
        # Clean up the downloaded zip file.
        path_ops.rm(fnm_zip_file)


def install_node():
    """Install fnm and nodejs for use by Reflex.
    Independent of any existing system installations.
    """
    if not constants.Fnm.FILENAME:
        # fnm only support Linux, macOS and Windows distros.
        console.debug("")
        return

    path_ops.mkdir(constants.Fnm.DIR)
    if not os.path.exists(constants.Fnm.EXE):
        download_and_extract_fnm_zip()

    if constants.IS_WINDOWS:
        # Install node
        fnm_exe = Path(constants.Fnm.EXE).resolve()
        fnm_dir = Path(constants.Fnm.DIR).resolve()
        process = processes.new_process(
            [
                "powershell",
                "-Command",
                f'& "{fnm_exe}" install {constants.Node.VERSION} --fnm-dir "{fnm_dir}"',
            ],
        )
    else:  # All other platforms (Linux, MacOS).
        # TODO we can skip installation if check_node_version() checks out
        # Add execute permissions to fnm executable.
        os.chmod(constants.Fnm.EXE, stat.S_IXUSR)
        # Install node.
        # Specify arm64 arch explicitly for M1s and M2s.
        architecture_arg = (
            ["--arch=arm64"]
            if platform.system() == "Darwin" and platform.machine() == "arm64"
            else []
        )

        process = processes.new_process(
            [
                constants.Fnm.EXE,
                "install",
                *architecture_arg,
                constants.Node.VERSION,
                "--fnm-dir",
                constants.Fnm.DIR,
            ],
        )
    processes.show_status("Installing node", process)


def install_bun():
    """Install bun onto the user's system.

    Raises:
        FileNotFoundError: If required packages are not found.
    """
    # Bun is not supported on Windows.
    if constants.IS_WINDOWS:
        console.debug("Skipping bun installation on Windows.")
        return

    # Skip if bun is already installed.
    if os.path.exists(get_config().bun_path) and get_bun_version() == version.parse(
        constants.Bun.VERSION
    ):
        console.debug("Skipping bun installation as it is already installed.")
        return

    #  if unzip is installed
    unzip_path = path_ops.which("unzip")
    if unzip_path is None:
        raise FileNotFoundError("Reflex requires unzip to be installed.")

    # Run the bun install script.
    download_and_run(
        constants.Bun.INSTALL_URL,
        f"bun-v{constants.Bun.VERSION}",
        BUN_INSTALL=constants.Bun.ROOT_PATH,
    )


def install_frontend_packages(packages: set[str]):
    """Installs the base and custom frontend packages.

    Args:
        packages: A list of package names to be installed.

    Example:
        >>> install_frontend_packages(["react", "react-dom"])
    """
    # Install the base packages.
    process = processes.new_process(
        [get_install_package_manager(), "install", "--loglevel", "silly"],
        cwd=constants.Dirs.WEB,
        shell=constants.IS_WINDOWS,
    )

    processes.show_status("Installing base frontend packages", process)

    config = get_config()
    if config.tailwind is not None:
        # install tailwind and tailwind plugins as dev dependencies.
        process = processes.new_process(
            [
                get_install_package_manager(),
                "add",
                "-d",
                constants.Tailwind.VERSION,
                *((config.tailwind or {}).get("plugins", [])),
            ],
            cwd=constants.Dirs.WEB,
            shell=constants.IS_WINDOWS,
        )
        processes.show_status("Installing tailwind", process)

    # Install custom packages defined in frontend_packages
    if len(packages) > 0:
        process = processes.new_process(
            [get_install_package_manager(), "add", *packages],
            cwd=constants.Dirs.WEB,
            shell=constants.IS_WINDOWS,
        )
        processes.show_status(
            "Installing frontend packages from config and components", process
        )


def check_initialized(frontend: bool = True):
    """Check that the app is initialized.

    Args:
        frontend: Whether to check if the frontend is initialized.

    Raises:
        Exit: If the app is not initialized.
    """
    has_config = os.path.exists(constants.Config.FILE)
    has_reflex_dir = not frontend or os.path.exists(constants.Reflex.DIR)
    has_web_dir = not frontend or os.path.exists(constants.Dirs.WEB)

    # Check if the app is initialized.
    if not (has_config and has_reflex_dir and has_web_dir):
        console.error(
            f"The app is not initialized. Run [bold]{constants.Reflex.MODULE_NAME} init[/bold] first."
        )
        raise typer.Exit(1)

    # Check that the template is up to date.
    if frontend and not is_latest_template():
        console.error(
            "The base app template has updated. Run [bold]reflex init[/bold] again."
        )
        raise typer.Exit(1)

    # Print a warning for Windows users.
    if constants.IS_WINDOWS:
        console.warn(
            """Windows Subsystem for Linux (WSL) is recommended for improving initial install times."""
        )


def is_latest_template() -> bool:
    """Whether the app is using the latest template.

    Returns:
        Whether the app is using the latest template.
    """
    if not os.path.exists(constants.Reflex.JSON):
        return False
    with open(constants.Reflex.JSON) as f:  # type: ignore
        app_version = json.load(f)["version"]
    return app_version == constants.Reflex.VERSION


def validate_bun():
    """Validate bun if a custom bun path is specified to ensure the bun version meets requirements.

    Raises:
        Exit: If custom specified bun does not exist or does not meet requirements.
    """
    # if a custom bun path is provided, make sure its valid
    # This is specific to non-FHS OS
    bun_path = get_config().bun_path
    if bun_path != constants.Bun.DEFAULT_PATH:
        bun_version = get_bun_version()
        if not bun_version:
            console.error(
                "Failed to obtain bun version. Make sure the specified bun path in your config is correct."
            )
            raise typer.Exit(1)
        elif bun_version < version.parse(constants.Bun.MIN_VERSION):
            console.error(
                f"Reflex requires bun version {constants.Bun.VERSION} or higher to run, but the detected version is "
                f"{bun_version}. If you have specified a custom bun path in your config, make sure to provide one "
                f"that satisfies the minimum version requirement."
            )

            raise typer.Exit(1)


def validate_frontend_dependencies(init=True):
    """Validate frontend dependencies to ensure they meet requirements.

    Args:
        init: whether running `reflex init`

    Raises:
        Exit: If the package manager is invalid.
    """
    if not init:
        # we only need to validate the package manager when running app.
        # `reflex init` will install the deps anyway(if applied).
        package_manager = get_package_manager()
        if not package_manager:
            console.error(
                "Could not find NPM package manager. Make sure you have node installed."
            )
            raise typer.Exit(1)

        if not check_node_version():
            node_version = get_node_version()
            console.error(
                f"Reflex requires node version {constants.Node.MIN_VERSION} or higher to run, but the detected version is {node_version}",
            )
            raise typer.Exit(1)

    if constants.IS_WINDOWS:
        return

    if init:
        # we only need bun for package install on `reflex init`.
        validate_bun()


def initialize_frontend_dependencies():
    """Initialize all the frontend dependencies."""
    # Create the reflex directory.
    path_ops.mkdir(constants.Reflex.DIR)
    # validate dependencies before install
    validate_frontend_dependencies()
    # Install the frontend dependencies.
    processes.run_concurrently(install_node, install_bun)
    # Set up the web directory.
    initialize_web_directory()


def check_db_initialized() -> bool:
    """Check if the database migrations are initialized.

    Returns:
        True if alembic is initialized (or if database is not used).
    """
    if get_config().db_url is not None and not Path(constants.ALEMBIC_CONFIG).exists():
        console.error(
            "Database is not initialized. Run [bold]reflex db init[/bold] first."
        )
        return False
    return True


def check_schema_up_to_date():
    """Check if the sqlmodel metadata matches the current database schema."""
    if get_config().db_url is None or not Path(constants.ALEMBIC_CONFIG).exists():
        return
    with model.Model.get_db_engine().connect() as connection:
        try:
            if model.Model.alembic_autogenerate(
                connection=connection,
                write_migration_scripts=False,
            ):
                console.error(
                    "Detected database schema changes. Run [bold]reflex db makemigrations[/bold] "
                    "to generate migration scripts.",
                )
        except CommandError as command_error:
            if "Target database is not up to date." in str(command_error):
                console.error(
                    f"{command_error} Run [bold]reflex db migrate[/bold] to update database."
                )


def prompt_for_template() -> constants.Templates.Kind:
    """Prompt the user to specify a template.

    Returns:
        The template the user selected.
    """
    # Show the user the URLs of each temlate to preview.
    console.print("\nGet started with a template:")
    console.print("blank (https://blank-template.reflex.run) - A minimal template.")
    console.print(
        "sidebar (https://sidebar-template.reflex.run) - A template with a sidebar to navigate pages."
    )
    console.print("")

    # Prompt the user to select a template.
    template = console.ask(
        "Which template would you like to use?",
        choices=[
            template.value
            for template in constants.Templates.Kind
            if template.value != "demo"
        ],
        default=constants.Templates.Kind.BLANK.value,
    )

    # Return the template.
    return constants.Templates.Kind(template)


def migrate_to_reflex():
    """Migration from Pynecone to Reflex."""
    # Check if the old config file exists.
    if not os.path.exists(constants.Config.PREVIOUS_FILE):
        return

    # Ask the user if they want to migrate.
    action = console.ask(
        "Pynecone project detected. Automatically upgrade to Reflex?",
        choices=["y", "n"],
    )
    if action == "n":
        return

    # Rename pcconfig to rxconfig.
    console.log(
        f"[bold]Renaming {constants.Config.PREVIOUS_FILE} to {constants.Config.FILE}"
    )
    os.rename(constants.Config.PREVIOUS_FILE, constants.Config.FILE)

    # Find all python files in the app directory.
    file_pattern = os.path.join(get_config().app_name, "**/*.py")
    file_list = glob.glob(file_pattern, recursive=True)

    # Add the config file to the list of files to be migrated.
    file_list.append(constants.Config.FILE)

    # Migrate all files.
    updates = {
        "Pynecone": "Reflex",
        "pynecone as pc": "reflex as rx",
        "pynecone.io": "reflex.dev",
        "pynecone": "reflex",
        "pc.": "rx.",
        "pcconfig": "rxconfig",
    }
    for file_path in file_list:
        with FileInput(file_path, inplace=True) as file:
            for line in file:
                for old, new in updates.items():
                    line = line.replace(old, new)
                print(line, end="")
