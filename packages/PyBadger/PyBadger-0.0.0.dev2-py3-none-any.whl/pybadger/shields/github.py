
class GitHub:
    """GitHub Badges."""

    def __init__(
        self,
        user: str,
        repo: str,
        branch: Optional[str] = None,
        default_logo: bool = True,
        **kwargs,
    ):
        """
        Parameters
        ----------
        user : str
            GitHub username.
        repo : str
            GitHub repository name.
        branch : str, optional
            GitHub branch name.
        default_logo : bool, default: True
            Whether to add a white GitHub logo to all badges by default.
            This will have no effect if 'logo' is provided as a keyword argument.
        **kwargs
            Any other argument accepted by `ShieldsBadge`. These will be used as default values
            for all badges, unless the same argument is also provided to the method when creating a specific badge,
            in which case, the default value will be overridden.
        """
        self.user = user
        self.repo = repo
        self.branch = branch
        self._url = _BASE_URL / "github"
        self._address = f"{user}/{repo}"
        self._repo_link = pylinks.github.user(user).repo(repo)
        if default_logo and "logo" not in kwargs:
            kwargs["logo"] = {"simple_icons": "github", "color": "white"}
        self.args = kwargs
        return

    def workflow_status(
        self,
        filename: str,
        description: Optional[str] = None,
        **kwargs,
    ) -> ShieldsBadge:
        """Status (failing/passing) of a GitHub workflow.

        Parameters
        ----------
        filename : str
            Full filename of the workflow, e.g. 'ci.yaml'.
        description : str, optional
            A description for the workflow.
            This will be used for the 'title' attribute of the badge's 'img' element, unless 'title'
            is provided as a keyword argument.
        """
        path = self._url / "actions/workflow/status" / self._address / filename
        link = self._repo_link.workflow(filename)
        if self.branch:
            path.queries["branch"] = self.branch
            link = self._repo_link.branch(self.branch).workflow(filename)
        args = self.args | kwargs
        if "title" not in args:
            args["title"] = (
                f"Status of the GitHub Actions workflow '{filename}'"
                f"""{f"on branch '{self.branch}'" if self.branch else ''}. """
                f"""{f"{description.strip().rstrip('.')}. " if description else ""}"""
                "Click to see more details in the Actions section of the repository."
            )
        if "alt" not in args and "text" not in args:
            args["alt"] = "GitHub Workflow Status"
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def pr_issue(
        self,
        pr: bool = True,
        status: Literal["open", "closed", "both"] = "both",
        label: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> ShieldsBadge:
        """Number of pull requests or issues on GitHub.

        Parameters
        ----------
        pr : bool, default: True
            Whether to query pull requests (True, default) or issues (False).
        closed : bool, default: False
            Whether to query closed (True) or open (False, default) issues/pull requests.
        label : str, optional
            A specific GitHub label to query.
        raw : bool, default: False
            Display 'open'/'close' after the number (False) or only display the number (True).
        """

        def get_path_link(closed):
            path = self._url / (
                f"issues{'-pr' if pr else ''}{'-closed' if closed else ''}"
                f"{'-raw' if raw else ''}/{self._address}{f'/{label}' if label else ''}"
            )
            link = self._repo_link.pr_issues(pr=pr, closed=closed, label=label)
            return path, link

        def half_badge(closed: bool):
            path, link = get_path_link(closed=closed)
            if "link" not in args:
                args["link"] = link
            badge = ShieldsBadge(path=path, **args)
            badge.html_syntax = ""
            if closed:
                badge.color = {"right": "00802b"}
                badge.text = ""
                badge.logo = None
            else:
                badge.color = {"right": "AF1F10"}
            return badge

        desc = {
            None: {True: "pull requests in total", False: "issues in total"},
            "bug": {True: "pull requests related to a bug-fix", False: "bug-related issues"},
            "enhancement": {
                True: "pull requests related to new features and enhancements",
                False: "feature and enhancement requests",
            },
            "documentation": {
                True: "pull requests related to the documentation",
                False: "issues related to the documentation",
            },
        }
        text = {
            None: {True: "Total", False: "Total"},
            "bug": {True: "Bug Fix", False: "Bug Report"},
            "enhancement": {True: "Enhancement", False: "Feature Request"},
            "documentation": {True: "Docs", False: "Docs"},
        }

        args = self.args | kwargs
        if "text" not in args:
            args["text"] = text[label][pr]
        if "title" not in args:
            args["title"] = (
                f"Number of {status if status != 'both' else 'open (red) and closed (green)'} "
                f"{desc[label][pr]}. "
                f"Click {'on the red and green tags' if status=='both' else ''} to see the details of "
                f"the respective {'pull requests' if pr else 'issues'} in the "
                f"'{'Pull requests' if pr else 'Issues'}' section of the repository."
            )
        if "style" not in args and status == "both":
            args["style"] = "flat-square"
        if status not in ("open", "closed", "both"):
            raise ValueError()
        if status != "both":
            path, link = get_path_link(closed=status == "closed")
            if "link" not in args:
                args["link"] = link
            return ShieldsBadge(path=path, **args)
        return html.element.ElementCollection(
            [half_badge(closed) for closed in (False, True)], seperator=""
        )

    def top_language(self, **kwargs) -> ShieldsBadge:
        """The top language in the repository, and its frequency."""
        args = self.args | kwargs
        if "alt" not in args:
            args["alt"] = "Top Programming Language"
        if "title" not in args:
            args["title"] = "Percentage of the most used programming language in the repository."
        return ShieldsBadge(path=self._url / "languages/top" / self._address, **args)

    def language_count(self, **kwargs) -> ShieldsBadge:
        """Number of programming languages used in the repository."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Programming Languages"
        if "title" not in args:
            args["title"] = "Number of programming languages used in the repository."
        return ShieldsBadge(path=self._url / "languages/count/" / self._address, **args)

    def downloads(
        self,
        tag: Optional[str | Literal["latest"]] = None,
        asset: Optional[str] = None,
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ) -> ShieldsBadge:
        """
        Number of downloads of a GitHub release.

        Parameters
        ----------
        tag : str, default: None
            A specific release tag to query. If set to None (default), number of total downloads is displayed.
            Additionally, the keyword 'latest' can be provided to query the latest release.
        asset : str, optional
            An optional asset to query.
        include_pre_release : bool, default: True
            Whether to include pre-releases in the count.
        sort_by_semver : bool, default: False
            If tag is set to 'latest', whether to choose the latest release according
            to the Semantic Versioning (True), or according to date (False).
        """
        path = self._url / f"downloads{'-pre' if include_pre_release else ''}/{self._address}"
        if not tag:
            path /= "total"
        else:
            path /= f'{tag}/{asset if asset else "total"}'
            if sort_by_semver:
                path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            if tag:
                target = (
                    f" for the {'latest release' if tag == 'latest' else f'release version {tag}'}"
                )
                if asset:
                    target += f" and asset '{asset}'"
            elif asset:
                target = f" for the asset {asset}"
            args["title"] = (
                f"Number of {'total ' if not (asset or tag) else ''}GitHub downloads{target}. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag=tag if tag else "latest")
        return ShieldsBadge(path=path, **args)

    def license(self, filename: str = "LICENSE", branch: str = "main", **kwargs) -> ShieldsBadge:
        """License of the GitHub repository.

        Parameters
        ----------
        filename : str, default: 'LICENSE'
            Name of the license file in the GitHub branch.
            This is used to create a link to the license.
        """
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "License"
        if "title" not in args:
            args["title"] = "License of the project. Click to read the complete license."
        if "link" not in args:
            args["link"] = self._repo_link.branch(self.branch or branch).file(filename)
        return ShieldsBadge(path=self._url / "license" / self._address, **args)

    def commit_activity(self, interval: Literal["y", "m", "w"] = "m", **kwargs) -> ShieldsBadge:
        interval_text = {"y": "year", "m": "month", "w": "week"}
        path = self._url / "commit-activity" / interval / self._address
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Commits"
        if "title" not in args:
            args["title"] = (
                f"""Average number of commits {f"in branch '{self.branch}' " if self.branch else ''}"""
                f"per {interval_text[interval]}. Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def commits_since(
        self,
        version: str | Literal["latest"] = "latest",
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ):
        path = self._url / "commits-since" / self._address / version
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        if include_pre_release:
            path.queries["include_prereleases"] = None
        if sort_by_semver:
            path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args and "alt" not in args:
            args[
                "alt"
            ] = f"Commits since {'latest release' if version=='latest' else f'release version {version}'}"
        if "title" not in args:
            args["title"] = (
                f"Number of commits since {'latest release' if version == 'latest' else f'release version {version}'}."
                "Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def last_commit(self, **kwargs):
        path = self._url / "last-commit" / self._address
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Last Commit"
        if "title" not in args:
            args["title"] = (
                f"""Time of last commit{f" on branch '{self.branch}'" if self.branch else ''}."""
                "Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def release_date(
        self, pre_release: bool = True, publish_date: bool = False, **kwargs
    ) -> ShieldsBadge:
        """
        Release date (optionally publish date) of the latest released version on GitHub.

        Parameters
        ----------
        pre_release : bool, default: True
            Whether to include pre-releases.
        publish_date : bool, default: False
            Get publish date instead of release date.
        kwargs
            Any other argument accepted by `ShieldsBadge`.
        """
        path = self._url / ("release-date-pre" if pre_release else "release-date") / self._address
        if publish_date:
            path.queries["display_date"] = "published_at"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Released"
        if "alt" not in args:
            args["alt"] = "Release Date"
        if "title" not in args:
            args["title"] = (
                "Release date of the latest version. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag="latest")
        return ShieldsBadge(path=path, **args)

    def release_version(
        self,
        display_name: Optional[Literal["tag", "release"]] = None,
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ):
        path = self._url / "v/release" / self._address
        if display_name:
            path.queries["display_name"] = display_name
        if include_pre_release:
            path.queries["include_prereleases"] = None
        if sort_by_semver:
            path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Version"
        if "title" not in args:
            args["title"] = (
                "Latest release version. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag="latest")
        return ShieldsBadge(path=path, **args)

    def code_size(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Code Size"
        if "title" not in args:
            args["title"] = "Total size of all source files in the repository."
        return ShieldsBadge(path=self._url / "languages/code-size" / self._address, **args)

    def dir_file_count(
        self,
        path: Optional[str] = None,
        selection: Optional[Literal["file", "dir"]] = None,
        file_extension: Optional[str] = None,
        **kwargs,
    ):
        img_path = self._url / "directory-file-count" / self._address
        if path:
            img_path /= path
        if selection:
            img_path.queries["type"] = selection
        if file_extension:
            img_path.queries["extension"] = file_extension
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Files"
        if "title" not in args:
            things = (
                "files and directories"
                if not selection
                else ("files" if selection == "file" else "directories")
            )
            args["title"] = (
                f"Total number of {things} "
                f"""{f"with the extension '{file_extension}' " if file_extension else ''}"""
                f"""{f"located under '{path}'" if path else 'in the repository'}."""
            )
        return ShieldsBadge(img_path, **args)

    def repo_size(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Repo Size"
        if "title" not in args:
            args["title"] = "Total size of the repository."
        return ShieldsBadge(self._url / "repo-size" / self._address, **args)

    def milestones(self, state: Literal["open", "closed", "both", "all"] = "all", **kwargs):
        def get_path_link(state):
            path = self._url / "milestones" / state / self._address
            link = self._repo_link.milestones(state=state if state == "closed" else "open")
            return path, link

        def half_badge(state):
            path, link = get_path_link(state=state)
            if "link" not in args:
                args["link"] = link
            badge = ShieldsBadge(path=path, **args)
            badge.html_syntax = ""
            if state == "closed":
                badge.color = {"right": "00802b"}
                badge.text = ""
                badge.logo = None
            else:
                badge.color = {"right": "AF1F10"}
            return badge

        args = self.args | kwargs
        if "text" not in args:
            args["text"] = (
                "Milestones"
                if state in ("all", "both")
                else ("Open Milestones" if state == "open" else "Finished Milestones")
            )
        if "title" not in args:
            which = (
                state
                if state not in ("both", "all")
                else ("open (red) and closed (green)" if state == "both" else "total")
            )
            args["title"] = (
                f"Number of {which} milestones. "
                f"Click {'on the red and green tags' if state == 'both' else ''} for more details."
            )
        if state != "both":
            path, link = get_path_link(state=state)
            if "link" not in args:
                args["link"] = link
            return ShieldsBadge(path=path, **args)
        return html.element.ElementCollection(
            [half_badge(state) for state in ("open", "closed")], seperator=""
        )

    def discussions(self, **kwargs) -> ShieldsBadge:
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Discussions"
        if "title" not in args:
            args[
                "title"
            ] = "Total number of discussions. Click to open the 'Discussions' section of the repository."
        if "link" not in args:
            args["link"] = self._repo_link.discussions()
        return ShieldsBadge(path=self._url / "discussions" / self._address, **args)

    def dependency_status(self, **kwargs) -> ShieldsBadge:
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        return ShieldsBadge(_BASE_URL / "librariesio/github" / self._address, **args)
