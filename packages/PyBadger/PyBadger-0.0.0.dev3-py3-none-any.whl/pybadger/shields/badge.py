# Standard libraries
import base64
import copy
from typing import Literal, Optional, Sequence
from pathlib import Path
# Non-standard libraries
from markitup import html
import pylinks
from pybadger.badge import Badge
from pylinks import url
from pylinks.url import URL


def _process_logo(logo: str | Path | URL | tuple[str, str | bytes | Path | URL]):

    mime_type = {
        "apng": "image/apng",
        "avif": "image/avif",
        "bmp": "image/bmp",
        "gif": "image/gif",
        "ico": "image/x-icon",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "svg": "image/svg+xml",
        "tif": "image/tiff",
        "tiff": "image/tiff",
        "webp": "image/webp",
    }

    def encode_logo(content, mime_type: str = "png"):
        return f'data:{mime_type};base64,{base64.b64encode(content).decode()}'

    if isinstance(logo, tuple):
        if len(logo) != 2:
            raise ValueError()
        extension = logo[0]
        data = logo[1]
        if extension not in mime_type:
            raise ValueError(f"Logo extension '{extension}' is not recognized.")
    else:
        extension = None
        data = logo

    if isinstance(data, str):
        if data.startswith(("http://", "https://")):
            content = pylinks.http.request(url=data, response_type="bytes")
            extension = extension or logo.rsplit(".", 1)[-1]
            if extension not in mime_type:
                raise ValueError(f"Logo extension '{extension}' is not recognized.")
            return encode_logo(content, mime_type=mime_type[extension])
        return data

    if isinstance(data, bytes):
        if extension is None:
            raise ValueError()
        return encode_logo(data, mime_type=mime_type[extension])

    if isinstance(data, Path):
        content = data.read_bytes()
        extension = extension or logo.suffix[1:]
        if extension not in mime_type:
            raise ValueError(f"Logo extension '{extension}' is not recognized.")
        return encode_logo(content, mime_type=mime_type[extension])

    if isinstance(data, URL):
        content = pylinks.http.request(url=data, response_type="bytes")
        extension = extension or str(data).rsplit(".", 1)[-1]
        if extension not in mime_type:
            raise ValueError(f"Logo extension '{extension}' is not recognized.")
        return encode_logo(content, mime_type=mime_type[extension])

    raise ValueError(f"Logo type '{type(logo)}' is not recognized.")

    # if not isinstance(value, dict):
    #     raise ValueError(f"`logo` expects either a string or a dict, but got {type(value)}.")
    # for key, val in value.items():
    #     if key == "width":
    #         self._logo["width"] = val
    #     elif key == "color":
    #         if isinstance(val, str):
    #             self._logo["color"] = {"dark": val, "light": val}
    #         elif isinstance(val, dict):
    #             for key2, val2 in val.items():
    #                 if key2 not in ("dark", "light"):
    #                     raise ValueError()
    #                 self._logo["color"][key2] = val2
    #         else:
    #             raise ValueError()
    #     elif key == "simple_icons":
    #         self._logo["data"] = val
    #     elif key == "url":
    #         content = pylinks.http.request(url=val, response_type="bytes")
    #         self._logo["data"] = encode_logo(content)
    #     elif key == "local":
    #         with open(val["value"], "rb") as f:
    #             content = f.read()
    #             self._logo = encode_logo(content)
    #     elif key == "bytes":
    #         self._logo = encode_logo(content)
    #     elif key == "github":
    #         content = pylinks.http.request(
    #             url=pylinks.github.user(val["user"])
    #             .repo(val["repo"])
    #             .branch(val["branch"])
    #             .file(val["path"], raw=True),
    #             response_type="bytes",
    #         )
    #         self._logo["data"] = encode_logo(content)
    #     else:
    #         raise ValueError(f"Key '{key}' in logo spec. {value} is not recognized.")
    # return


def badge(
    path: str,
    style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] | None,
    message: str | None = None,
    color: str | None = None,
    label: str | None = None,
    label_color: str | None = None,
    logo: str | Path | URL | tuple[str, str | bytes | Path | URL] | None = None,
    logo_color: str | None = None,
    logo_width: int | None = None,
    link: str | URL | None = None,
    cache_seconds: int | None = None,
):
    _url = url("https://img.shields.io") / path
    if logo:
        logo = _process_logo(logo)
    for key, val in (
        ("style", style),
        ("message", message),
        ("color", color),
        ("label", label),
        ("labelColor", label_color),
        ("logo", logo),
        ("logoColor", logo_color),
        ("logoWidth", logo_width),
        ("link", link),
        ("cacheSeconds", cache_seconds),
    ):
        if val is not None:
            _url.queries[key] = val
    return Badge(url=_url, link=link)



class ShieldsBadge(Badge):
    """SHIELDS.IO Badge"""

    def __init__(
        self,
        path: str,
        style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = None,
        text: str | dict[Literal["left", "right"], str] = None,
        logo: str | tuple[str, str] = None,
        color: str | dict[str, str | dict[str, str]] = None,
        cache_time: int = None,
        alt: str = None,
        title: str = None,
        width: str = None,
        height: str = None,
        align: str = None,
        link: str | URL = None,
        default_theme: Literal["light", "dark"] = "light",
        html_syntax: str | dict[Literal["tag_seperator", "content_indent"], str] = None,
    ):
        """
        Parameters
        ----------
        path : pylinks.URL
            Clean URL (without additional queries) of the badge image.
        style : {'plastic', 'flat', 'flat-square', 'for-the-badge', 'social'}
            Style of the badge.
        left_text : str
            Text on the left-hand side of the badge. Pass an empty string to omit the left side.
        right_text : str
            Text on the right-hand side of the badge. This can only be set for static badges.
            When `left_text` is set to empty string, this will be the only text shown.
        logo : str
            Logo on the badge. Two forms of input are accepted:
            1. A SimpleIcons icon name (see: https://simpleicons.org/), e.g. 'github',
                or one of the following names: 'bitcoin', 'dependabot', 'gitlab', 'npm', 'paypal',
                'serverfault', 'stackexchange', 'superuser', 'telegram', 'travis'.
            2. A filepath to an image file; this must be inputted as a tuple, where the first
               element is the file extension, and the second element is the full path to the image file,
               e.g. `('png', '/home/pictures/my_logo.png')`.
        logo_width : float
            Horizontal space occupied by the logo.
        logo_color_light : str
            Color of the logo. This and other color inputs can be in one of the following forms:
            hex, rgb, rgba, hsl, hsla and css named colors.
        left_color_light : str
            Color of the left side. See `logo_color` for more detail.
        right_color_dark : str
            Color of the right side. See `logo_color` for more detail.
        cache_time : int
            HTTP cache lifetime in seconds.
        """

        self._url: URL = url("https://img.shields.io") / path
        self.style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = style

        self._text = self._init_text()
        self.text = text

        self._logo = self._init_logo()
        self.logo = logo

        self._color = self._init_color()
        self.color = color

        self.cache_time: int = cache_time

        if alt is not False:
            alt = alt or self.text["left"] or self.text["right"]
        super().__init__(
            alt=alt,
            title=title,
            width=width,
            height=height,
            align=align,
            link=link,
            default_theme=default_theme,
            html_syntax=html_syntax,
        )
        return

    def url(self, mode: Literal["light", "dark", "clean"] = "dark") -> URL:
        """
        URL of the badge image.

        Parameters
        ----------
        mode : {'dark', 'light', 'clean'}
            'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
            respectively, while 'clean' gives the URL of the badge image without any customization.

        Returns
        -------
        url : pylinks.url.URL
            A URL object, which among others, has a __str__ method to output the URL as a string.
        """
        url = self._url.copy()
        if mode == "clean":
            return url
        for key, val in (
            ("label", self.text["left"]),
            ("message", self.text["right"]),
            ("style", self.style),
            ("labelColor", self.color["left"][mode]),
            ("color", self.color["right"][mode]),
            ("logo", self.logo["data"]),
            ("logoColor", self.logo["color"][mode]),
            ("logoWidth", self.logo["width"]),
            ("cacheSeconds", self.cache_time),
        ):
            if val is not None:
                url.queries[key] = val
        return url

    @property
    def color(self):
        return copy.deepcopy(self._color)

    @color.setter
    def color(self, value):
        if value is None:
            self._color = self._init_color()
            return
        if isinstance(value, str):
            new_colors = {"dark": value, "light": value}
            if self._is_static and not self.text["left"]:
                self._color["right"] = new_colors
                return
            self._color["left"] = new_colors
            return
        if not isinstance(value, dict):
            return ValueError()
        for key, val in value.items():
            if key not in ("left", "right", "dark", "light"):
                raise ValueError()
            if isinstance(val, str):
                if key in ("left", "right"):
                    self._color[key] = {"dark": val, "light": val}
                else:
                    side = "right" if self._is_static and not self.text["left"] else "left"
                    self._color[side][key] = val
            elif isinstance(val, dict):
                for key2, val2 in val.items():
                    if key2 not in ("left", "right", "dark", "light"):
                        raise ValueError()
                    if key2 in ("dark", "light"):
                        if key in ("dark", "light"):
                            raise ValueError()
                        self._color[key][key2] = val2
                    else:
                        if key in ("left", "right"):
                            raise ValueError()
                        self._color[key2][key] = val2
            else:
                raise ValueError()
        return

    @property
    def text(self):
        return copy.deepcopy(self._text)

    @text.setter
    def text(self, value):
        if value is None:
            self._text = self._init_text()
            return
        if isinstance(value, str):
            if self._is_static:
                self._text = {"left": "", "right": value}
                return
            self._text["left"] = value
            return
        if not isinstance(value, dict):
            raise ValueError()
        for key, val in value.items():
            if key not in ("left", "right"):
                raise ValueError()
            if key == "right" and not self._is_static:
                raise ValueError()
            self._text[key] = val
        return

    @property
    def _is_static(self):
        return str(self._url).startswith("https://img.shields.io/static/")

    @staticmethod
    def _init_text():
        return {"left": None, "right": None}

    @staticmethod
    def _init_color():
        return {"left": {"dark": None, "light": None}, "right": {"dark": None, "light": None}}

    @staticmethod
    def _init_logo():
        return {"data": None, "width": None, "color": {"dark": None, "light": None}}
