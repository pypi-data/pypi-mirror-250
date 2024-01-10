from ..common import os


def directory_create(directory_name: str) -> bool:
    """
    指定ディレクトリの作成

    Parameters
    ----------
    directory_name : str
        作成したいディレクトリ名

    Returns
    -------
    bool
        成功可否

    Raises
    ------
    TypeError
        入力型がstrでない
    """
    _current_directory = os.getcwd()
    try:
        if not isinstance(directory_name, str):
            raise TypeError
        directory = os.path.join(_current_directory, directory_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except TypeError:
        return False
