"""Radix Icons."""


from typing import List

from reflex.components.component import Component
from reflex.utils import format


class RadixIconComponent(Component):
    """A component used as basis for Radix icons."""

    library = "@radix-ui/react-icons@^1.3.0"


class Icon(RadixIconComponent):
    """An image Icon."""

    tag = "None"

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Initialize the Icon component.

        Run some additional checks on Icon component.

        Args:
            *children: The positional arguments
            **props: The keyword arguments

        Raises:
            AttributeError: The errors tied to bad usage of the Icon component.
            ValueError: If the icon tag is invalid.

        Returns:
            The created component.
        """
        if children:
            raise AttributeError(
                f"Passing children to Icon component is not allowed: remove positional arguments {children} to fix"
            )
        if "tag" not in props.keys():
            raise AttributeError("Missing 'tag' keyword-argument for Icon")
        if type(props["tag"]) != str or props["tag"].lower() not in ICON_LIST:
            raise ValueError(
                f"Invalid icon tag: {props['tag']}. Please use one of the following: {sorted(ICON_LIST)}"
            )
        props["tag"] = format.to_title_case(props["tag"]) + "Icon"
        return super().create(*children, **props)


ICON_ABSTRACT: List[str] = [
    "hamburger_menu",
    "cross_1",
    "dots_vertical",
    "dots_horizontal",
    "plus",
    "minus",
    "check",
    "cross_2",
    "check_circled",
    "cross_circled",
    "plus_circled",
    "minus_circled",
    "question_mark",
    "question_mark_circled",
    "info_circled",
    "accessibility",
    "exclamation_triangle",
    "share_1",
    "share_2",
    "external_link",
    "open_in_new_window",
    "enter",
    "exit",
    "download",
    "upload",
    "reset",
    "reload",
    "update",
    "enter_full_screen",
    "exit_full_screen",
    "drag_handle_vertical",
    "drag_handle_horizontal",
    "drag_handle_dots_1",
    "drag_handle_dots_2",
    "dot",
    "dot_filled",
    "commit",
    "slash",
    "circle",
    "circle_backslash",
    "half_1",
    "half_2",
    "view_none",
    "view_horizontal",
    "view_vertical",
    "view_grid",
    "copy",
    "square",
]
ICON_ALIGNS: List[str] = [
    "align_top",
    "align_center_vertically",
    "align_bottom",
    "stretch_vertically",
    "align_left",
    "align_center_horizontally",
    "align_right",
    "stretch_horizontally",
    "space_between_horizontally",
    "space_evenly_horizontally",
    "space_between_vertically",
    "space_evenly_vertically",
    "pin_left",
    "pin_right",
    "pin_top",
    "pin_bottom",
]
ICON_ARROWS: List[str] = [
    "arrow_left",
    "arrow_right",
    "arrow_up",
    "arrow_down",
    "arrow_top_left",
    "arrow_top_right",
    "arrow_bottom_left",
    "arrow_bottom_right",
    "chevron_left",
    "chevron_right",
    "chevron_up",
    "chevron_down",
    "double_arrow_down",
    "double_arrow_right",
    "double_arrow_left",
    "double_arrow_up",
    "thick_arrow_up",
    "thick_arrow_down",
    "thick_arrow_right",
    "thick_arrow_left",
    "triangle_right",
    "triangle_left",
    "triangle_down",
    "triangle_up",
    "caret_down",
    "caret_up",
    "caret_left",
    "caret_right",
    "caret_sort",
    "width",
    "height",
    "size",
    "move",
    "all_sides",
]
ICON_BORDERS: List[str] = [
    "border_all",
    "border_split",
    "border_none",
    "border_left",
    "border_right",
    "border_top",
    "border_bottom",
    "border_width",
    "corners",
    "corner_top_left",
    "corner_top_right",
    "corner_bottom_right",
    "corner_bottom_left",
    "border_style",
    "border_solid",
    "border_dashed",
    "border_dotted",
]
ICON_COMPONENTS: List[str] = [
    "box",
    "aspect_ratio",
    "container",
    "section",
    "layout",
    "grid",
    "table",
    "image",
    "switch",
    "checkbox",
    "radiobutton",
    "avatar",
    "button",
    "badge",
    "input",
    "slider",
    "quote",
    "code",
    "list_bullet",
    "dropdown_menu",
    "video",
    "pie_chart",
    "calendar",
    "dashboard",
    "activity_log",
    "bar_chart",
    "divider_horizontal",
    "divider_vertical",
]
ICON_DESIGN: List[str] = [
    "frame",
    "crop",
    "layers",
    "stack",
    "tokens",
    "component_1",
    "component_2",
    "component_instance",
    "component_none",
    "component_boolean",
    "component_placeholder",
    "opacity",
    "blending_mode",
    "mask_on",
    "mask_off",
    "color_wheel",
    "shadow",
    "shadow_none",
    "shadow_inner",
    "shadow_outer",
    "value",
    "value_none",
    "zoom_in",
    "zoom_out",
    "transparency_grid",
    "group",
    "dimensions",
    "rotate_counter_clockwise",
    "columns",
    "rows",
    "transform",
    "box_model",
    "padding",
    "margin",
    "angle",
    "cursor_arrow",
    "cursor_text",
    "column_spacing",
    "row_spacing",
]
ICON_LOGOS: List[str] = [
    "modulz_logo",
    "stitches_logo",
    "figma_logo",
    "framer_logo",
    "sketch_logo",
    "twitter_logo",
    "icon_jar_logo",
    "git_hub_logo",
    "code_sandbox_logo",
    "notion_logo",
    "discord_logo",
    "instagram_logo",
    "linked_in_logo",
]
ICON_MUSIC: List[str] = [
    "play",
    "resume",
    "pause",
    "stop",
    "track_previous",
    "track_next",
    "loop",
    "shuffle",
    "speaker_loud",
    "speaker_moderate",
    "speaker_quiet",
    "speaker_off",
]
ICON_OBJECTS: List[str] = [
    "magnifying_glass",
    "gear",
    "bell",
    "home",
    "lock_closed",
    "lock_open_1",
    "lock_open_2",
    "backpack",
    "camera",
    "paper_plane",
    "rocket",
    "envelope_closed",
    "envelope_open",
    "chat_bubble",
    "link_1",
    "link_2",
    "link_break_1",
    "link_break_2",
    "link_none_1",
    "link_none_2",
    "trash",
    "pencil_1",
    "pencil_2",
    "bookmark",
    "bookmark_filled",
    "drawing_pin",
    "drawing_pin_filled",
    "sewing_pin",
    "sewing_pin_filled",
    "cube",
    "archive",
    "crumpled_paper",
    "mix",
    "mixer_horizontal",
    "mixer_vertical",
    "file",
    "file_minus",
    "file_plus",
    "file_text",
    "reader",
    "card_stack",
    "card_stack_plus",
    "card_stack_minus",
    "id_card",
    "crosshair_1",
    "crosshair_2",
    "target",
    "globe",
    "disc",
    "sun",
    "moon",
    "clock",
    "timer",
    "counter_clockwise_clock",
    "countdown_timer",
    "stopwatch",
    "lap_timer",
    "lightning_bolt",
    "magic_wand",
    "face",
    "person",
    "eye_open",
    "eye_none",
    "eye_closed",
    "hand",
    "ruler_horizontal",
    "ruler_square",
    "clipboard",
    "clipboard_copy",
    "desktop",
    "laptop",
    "mobile",
    "keyboard",
    "star",
    "star_filled",
    "heart",
    "heart_filled",
    "scissors",
    "hobby_knife",
    "eraser",
    "cookie",
]
ICON_TYPOGRAPHY: List[str] = [
    "font_style",
    "font_italic",
    "font_roman",
    "font_bold",
    "letter_case_lowercase",
    "letter_case_capitalize",
    "letter_case_uppercase",
    "letter_case_toggle",
    "letter_spacing",
    "align_baseline",
    "font_size",
    "font_family",
    "heading",
    "text",
    "text_none",
    "line_height",
    "underline",
    "strikethrough",
    "overline",
    "pilcrow",
    "text_align_left",
    "text_align_center",
    "text_align_right",
    "text_align_justify",
    "text_align_top",
    "text_align_middle",
    "text_align_bottom",
    "dash",
]

ICON_LIST: List[str] = [
    *ICON_ABSTRACT,
    *ICON_ALIGNS,
    *ICON_ARROWS,
    *ICON_BORDERS,
    *ICON_COMPONENTS,
    *ICON_DESIGN,
    *ICON_LOGOS,
    *ICON_MUSIC,
    *ICON_OBJECTS,
    *ICON_TYPOGRAPHY,
]
