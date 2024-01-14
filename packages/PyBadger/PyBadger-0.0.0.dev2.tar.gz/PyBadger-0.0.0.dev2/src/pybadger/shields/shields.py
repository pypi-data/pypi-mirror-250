"""
Dynamically create badges using the shields.io API

References
----------
* https://shields.io/
* https://github.com/badges/shields
"""


# Standard libraries
import base64
import copy
from typing import Literal, Optional, Sequence

# Non-standard libraries
from markitup import html
import pylinks
from pybadger import _badge
from pylinks import url
from pylinks.url import URL



class PyPI:
    def __init__(self, package_name: str, **kwargs):
        self.package_name = package_name
        self._url = _BASE_URL / "pypi"
        self._link = pylinks.pypi.package(package_name)
        self.args = kwargs
        return

    def downloads(self, period: Literal["dd", "dw", "dm"] = "dm", **kwargs):
        period_name = {"dd": "day", "dw": "week", "dm": "month"}
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            args["title"] = f"Average number of downloads per {period_name[period]} from PyPI."
            if "link" not in args:
                args["title"] += f" Click to open the package homepage on pypi.org."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / period / self.package_name, **args)

    def format(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Format"
        if "title" not in args:
            args["title"] = "Format of the PyPI package distribution."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "format" / self.package_name, **args)

    def development_status(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Development Status"
        if "title" not in args:
            args["title"] = "Current development phase of the project."
        return ShieldsBadge(self._url / "status" / self.package_name)

    def supported_python_versions(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Supports Python"
        if "title" not in args:
            args["title"] = "Supported Python versions of the latest release."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "pyversions" / self.package_name, **args)

    def version(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Version"
        if "title" not in args:
            args["title"] = "Latest release version on PyPI."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "v" / self.package_name, **args)


class Conda:
    def __init__(self, package_name: str, channel: str = "conda-forge", **kwargs):
        """
        Parameters
        ----------
        package_name : str
            Package name.
        channel : str, default: 'conda-forge'
            Channel name.
        """
        self.package_name = package_name
        self._channel = channel
        self._url = _BASE_URL / "conda"
        self._address = f"{channel}/{package_name}"
        self._link = pylinks.conda.package(name=package_name, channel=channel)
        self.args = kwargs
        return

    def downloads(self, **kwargs):
        """Number of total downloads."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            args["title"] = "Number of downloads for the Conda distribution."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "dn" / self._address, **args)

    def supported_platforms(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Platforms"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "pn" / self._address, **args)

    def version(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "v" / self._address, **args)


def build_read_the_docs(project: str, version: Optional[str] = None, **kwargs) -> ShieldsBadge:
    """Build status of a ReadTheDocs project.

    Parameters
    ----------
    project : str
        ReadTheDocs project name.
    version : str, optional
        Specific ReadTheDocs version of the documentation to query.
        https://img.shields.io/readthedocs/opencadd?logo=readthedocs&logoColor=%238CA1AF
    left_text : str, default = 'Website'
        Text on the left-hand side of the badge. If set to None, the shields.io default ('docs') will be selected.

    """
    if "text" not in kwargs:
        kwargs["text"] = "Website"
    if "alt" not in kwargs:
        kwargs["alt"] = "Website Build Status"
    if "title" not in kwargs:
        kwargs[
            "title"
        ] = "Website build status. Click to see more details on the ReadTheDocs platform."
    if "logo" not in kwargs:
        kwargs["logo"] = {"simple_icons": "readthedocs", "color": "FFF"}
    if "link" not in kwargs:
        kwargs["link"] = pylinks.readthedocs.project(project).build_status
    return ShieldsBadge(
        path=_BASE_URL / "readthedocs" / f"{project}{f'/{version}' if version else ''}", **kwargs
    )


def coverage_codecov(
    user: str,
    repo: str,
    branch: Optional[str] = None,
    vcs: Literal["github", "gitlab", "bitbucket"] = "github",
    **kwargs,
) -> ShieldsBadge:
    """Code coverage calculated by codecov.io.

    Parameters
    ----------
    user : str
        GitHub username
    repo : str
        GitHub repository name.
    branch : str, optional
        Name of specific branch to query.
    vcs : {'github', 'gitlab', 'bitbucket'}, default: 'github'
        Version control system hosting the repository.
    """
    abbr = {"github": "gh", "gitlab": "gl", "bitbucket": "bb"}
    if "text" not in kwargs:
        kwargs["text"] = "Code Coverage"
    if "title" not in kwargs:
        kwargs[
            "title"
        ] = "Source code coverage by the test suite. Click to see more details on codecov.io."
    if "logo" not in kwargs:
        kwargs["logo"] = {"simple_icons": "codecov", "color": "FFF"}
    if "link" not in kwargs:
        kwargs[
            "link"
        ] = f"https://codecov.io/{abbr[vcs]}/{user}/{repo}{f'/branch/{branch}' if branch else ''}"  # TODO: use PyLinks
    return ShieldsBadge(
        path=_BASE_URL / f"codecov/c/{vcs}/{user}/{repo}{f'/{branch}' if branch else ''}", **kwargs
    )


def chat_discord(server_id: str, **kwargs):
    """Number of online users in Discord server.

    Parameters
    ----------
    server_id : str
        Server ID of the Discord server, which can be located in the url of the channel.
        This is required in order access the Discord JSON API.

    Notes
    -----
    A Discord server admin must enable the widget setting on the server for this badge to work.
    This can be done in the Discord app: Server Setting > Widget > Enable Server Widget

    """
    return ShieldsBadge(path=_BASE_URL / "discord" / server_id, **kwargs)


def binder():
    logo = (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1"
        "olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1ol"
        "L1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspX"
        "msr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna3"
        "1Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHm"
        "Z4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8Zgms"
        "Nim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+"
        "n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk1"
        "7yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICA"
        "goiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v"
        "7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU"
        "66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sM"
        "vs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU6"
        "1tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtp"
        "BIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0"
        "kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGh"
        "ttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm"
        "+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+or"
        "HLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd"
        "7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y"
        "+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219"
        "IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo"
        "/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2"
        "QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+"
        "aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8S"
        "GSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/AD"
        "uTNKaQJdScAAAAAElFTkSuQmCC"
    )
    badge = static(right_text="binder", left_text="launch")
    badge.logo = logo
    badge.right_color_dark = badge.right_color_light = "579aca"
    badge.link = ""  # TODO
    return badge


class LibrariesIO:
    """Shields badges provided by Libraries.io."""

    def __init__(self, package_name: str, platform: str = "pypi", **kwargs):
        """
        Parameters
        ----------
        package_name : str
            Name of the package.
        platform : str, default: 'pypi'
            The platform where the package is distributed, e.g. 'pypi', 'conda' etc.
        """
        self.platform = platform
        self.package_name = package_name
        self._url = _BASE_URL / "librariesio"
        self._address = f"{platform}/{package_name}"
        self._link = URL(f"https://libraries.io/{platform}/{package_name}")
        self.args = kwargs
        return

    def dependency_status(self, version: Optional[str] = None, **kwargs) -> ShieldsBadge:
        """
        Dependency status of a package distributed on a package manager platform,
        obtained using Libraries.io.
        The right-hand text shows either 'up to date', or '{number} out of date'.

        Parameters
        ----------
        platform : str
            Name of a supported package manager, e.g. 'pypi', 'conda'.
        package_name : str
            Name of the package.
        version : str, optional
            A specific version to query.

        References
        ----------
        * https://libraries.io/
        """
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        path = self._url / "release" / self._address
        link = self._link
        if version:
            path /= version
            link /= f"{version}/tree"
        else:
            link /= "tree"
        if "link" not in kwargs:
            kwargs["link"] = link
        return ShieldsBadge(path, **args)

    def dependents(self, repo: bool = False, **kwargs) -> ShieldsBadge:
        """
        Number of packages or repositories that depend on this package.

        Parameters
        ----------
        repo : bool, default: False
            Whether to query repositories (True) or packages (False).
        """
        path = self._url / ("dependent-repos" if repo else "dependents") / self._address
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = f"Dependent {'Repos' if repo else 'Packages'}"
        if "title" not in args:
            args[
                "title"
            ] = f"Number of {'repositories' if repo else 'packages'} that have {self.package_name} as a dependency."
        if "link" not in kwargs:
            kwargs["link"] = self._link
        return ShieldsBadge(path, **args)

    def source_rank(self, **kwargs) -> ShieldsBadge:
        """SourceRank ranking of the package."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Source Rank"
        if "title" not in args:
            args["title"] = (
                "Ranking of the source code according to libraries.io SourceRank algorithm. "
                "Click to see more details on libraries.io website."
            )
        if "link" not in kwargs:
            kwargs["link"] = self._link / "sourcerank"
        return ShieldsBadge(self._url / "sourcerank" / self._address, **args)
