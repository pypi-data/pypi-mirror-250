"""Custom static, dynamic, and endpoint badges."""


from typing import Literal
from pathlib import Path
from pylinks.url import URL

from pybadger.badge import Badge
from pybadger.shields.badge import badge


def static(
    message: str,
    style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] | None = None,
    color: str | None = None,
    label: str | None = None,
    label_color: str | None = None,
    logo: str | Path | None = None,
    logo_color: str | None = None,
    logo_width: int | None = None,
    link: str | URL | None = None,
    cache_seconds: int | None = None,
) -> Badge:
    """Static badge with custom text on the right-hand side.

    Parameters
    ----------
    text : str | dict['left': str, 'right': str]
        The text on the badge. If a string is provided, the text on the right-hand side of
        the badge is set, and the left-hand side is omitted. Otherwise, a dictionary must be
        provided with keys 'left' and 'right', setting the text on both sides of the badge.
    **kwargs
        Any other argument accepted by `ShieldsBadge`.
    """
    attrs = locals()
    if attrs["label"] is None:
        attrs["label"] = ""
    return badge(path="static/v1", **attrs)
