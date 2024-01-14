from typing import Literal

from pybadger.pepy.badge import PePyBadge
from pylinks import url
from pylinks.url import URL


def downloads(
    package_name: str, period: Literal["total", "month", "week"] = "total"
) -> PePyBadge:
    """
    Number of downloads for a PyPI package.

    Parameters
    ----------
    package_name : str
        Name of the package.
    period : {'total', 'month', 'week'}, default: 'total'
        The period to query.
    """
    path = _BASE_URL / "personalized-badge" / package_name
    path.queries["period"] = period
    left_text = "Total Downloads" if period == "total" else f"Downloads/{period.capitalize()}"
    return PePyBadge(
        path=path,
        left_text=left_text,
        left_color_dark="grey",
        left_color_light="grey",
        link=url(f"https://pepy.tech/project/{package_name}?display=monthly"),
    )
