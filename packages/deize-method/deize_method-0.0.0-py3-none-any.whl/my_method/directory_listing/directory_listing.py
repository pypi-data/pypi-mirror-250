from ..common import Final, os


class DirectoryListing:
    _LISTING_ALL: Final[int] = 0
    _LISTING_FILE: Final[int] = 1
    _LISTING_DIR: Final[int] = 2

    @classmethod
    def file_listing(
        cls,
        source: str,
        targets: tuple[str] | str = ("",),
        exc_targets: tuple[str] | str = ("",),
    ) -> tuple[str]:
        """
        ファイル名リスト化メソッド

        Parameters
        ----------
        source : str
            リスト化ディレクトリパス
        target : tuple[str], optional
            検索文字列タプル, by default ()

        Returns
        -------
        tuple[str]
            リスト化
        """
        return cls._listing(source, cls._LISTING_FILE, targets, exc_targets)

    @classmethod
    def dir_listing(
        cls,
        source: str,
        targets: tuple[str] | str = ("",),
        exc_targets: tuple[str] | str = ("",),
    ) -> tuple[str]:
        """
        ディレクトリ名リスト化メソッド

        Parameters
        ----------
        source : str
            リスト化ディレクトリパス
        target : tuple[str], optional
            検索文字列タプル, by default ()

        Returns
        -------
        tuple[str]
            リスト化
        """
        return cls._listing(source, cls._LISTING_DIR, targets, exc_targets)

    @classmethod
    def all_listing(
        cls,
        source: str,
        targets: tuple[str] | str = ("",),
        exc_targets: tuple[str] | str = ("",),
    ) -> tuple[str]:
        """
        ファイル名、ディレクトリ名リスト化メソッド

        Parameters
        ----------
        source : str
            リスト化ディレクトリパス
        target : tuple[str], optional
            検索文字列タプル, by default ()

        Returns
        -------
        tuple[str]
            リスト化
        """
        return cls._listing(source, cls._LISTING_ALL, targets, exc_targets)

    @classmethod
    def _listing(
        cls,
        source: str,
        pattern: int,
        targets: tuple[str, ...] | str = ("",),
        exc_targets: tuple[str, ...] | str = ("",),
    ) -> tuple[str]:
        """
        _summary_

        Parameters
        ----------
        source : str
            _description_
        pattern : int
            _description_
        targets : tuple[str] | str, optional
            _description_, by default ("",)
        exc_targets : tuple[str] | str, optional
            _description_, by default ("",)

        Returns
        -------
        tuple[str]
            _description_
        """
        global _LISTING_DIR, _LISTING_FILE, _LISTING_ALL
        targets, exc_targets = cls._str_to_tuple(targets, exc_targets)
        files: list[str] = []
        for name in os.listdir(source):
            file_path = os.path.join(source, name)
            if pattern == cls._LISTING_DIR:
                is_pattern = os.path.isdir(file_path)
            elif pattern == cls._LISTING_FILE:
                is_pattern = os.path.isfile(file_path)
            elif pattern == cls._LISTING_ALL:
                is_pattern = True
            else:
                is_pattern = False
            has_target = any(target in name for target in targets)
            has_exc_target = any(exc_target in name for exc_target in exc_targets) and exc_targets != ("",)
            if is_pattern and has_target and not has_exc_target:
                files.append(name)
        return tuple(files)  # type: ignore[return-value]

    @staticmethod
    def _str_to_tuple(
        targets: tuple[str, ...] | str,
        exc_targets: tuple[str, ...] | str,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """
        文字列からタプルに変更する関数

        Parameters
        ----------
        targets : tuple[str] | str
            検索文字列、タプル
        exc_targets : tuple[str] | str
            除外文字列、タプル

        Returns
        -------
        tuple[tuple[str], tuple[str]]
            targets, exc_targets
        """
        if isinstance(targets, str):
            targets = (targets,)
        if isinstance(exc_targets, str):
            exc_targets = (exc_targets,)
        return (targets, exc_targets)
