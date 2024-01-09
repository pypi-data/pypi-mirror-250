"""Components for rendering heading.

https://www.radix-ui.com/themes/docs/theme/typography
"""
from __future__ import annotations

from reflex import el
from reflex.vars import Var

from ..base import (
    CommonMarginProps,
    LiteralAccentColor,
    RadixThemesComponent,
)
from .base import (
    LiteralTextSize,
    LiteralTextWeight,
)


class Blockquote(el.Blockquote, CommonMarginProps, RadixThemesComponent):
    """A block level extended quotation."""

    tag = "Blockquote"

    # Text size: "1" - "9"
    size: Var[LiteralTextSize]

    # Thickness of text: "light" | "regular" | "medium" | "bold"
    weight: Var[LiteralTextWeight]

    # Overrides the accent color inherited from the Theme.
    color: Var[LiteralAccentColor]

    # Whether to render the text with higher contrast color
    high_contrast: Var[bool]
