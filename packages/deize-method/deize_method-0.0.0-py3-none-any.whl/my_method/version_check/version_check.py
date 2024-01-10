from ..common import subprocess, time


class VersionCheck:
    def __init__(
        self,
        url: str = "",
        version: str = "",
    ) -> None:
        """
        バージョンチェックを行うクラス

        Parameters
        ----------
        url : str, optional
            リモートリポジトリのURL, by default ""
        version : str, optional
            バージョン情報, by default ""
        """
        self._url = url
        self._version = version

    def __call__(self) -> bool:
        """
        バージョンチェックを行う

        Returns
        -------
        bool
            成功可否
        """
        return self.check_version()

    def check_version(self) -> bool:
        """
        バージョンチェックを行う

        Returns
        -------
        bool
            成功可否
        """
        if not self._version:
            return False
        for _ in range(5):
            try:
                if self._url:
                    ls_remote = subprocess.check_output(
                        ["git", "ls-remote", "--tags", "--refs", self._url], encoding="utf-8"
                    ).strip()
                else:
                    ls_remote = subprocess.check_output(
                        ["git", "ls-remote", "--tags", "--refs"], encoding="utf-8"
                    ).strip()
                break
            except subprocess.CalledProcessError:
                time.sleep(0.5)
        else:
            ls_remote = "unknown"
        return self._version in ls_remote
