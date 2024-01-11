from ..common import Union, datetime


def input_int(print_str: str, unit: str = "") -> int:
    """
    int入力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    int
        入力数字
    """
    return _input(print_str=print_str, type=int, unit=unit)


def input_float(print_str: str, unit: str = "") -> float:
    """
    float入力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    float
        入力数字
    """
    return _input(print_str=print_str, type=float, unit=unit)


def input_str(print_str: str, unit: str = "") -> str:
    """
    文字列出力

    Parameters
    ----------
    print_str : str
        表示文字列
    unit : str
        単位 by default ""

    Returns
    -------
    str
        入力文字列
    """
    return _input(print_str=print_str, type=str, unit=unit)


def input_min_sec(print_str: str) -> datetime:
    """
    入力時間からdatetimeオブジェクトを出力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    int
        _description_
    """
    return _input(print_str=print_str, type=datetime)


def input_bool(print_str: str) -> bool:
    """
    bool入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    bool
        入力bool
    """
    return _input(print_str=print_str, type=bool)


def _input(
    print_str: str,
    type: Union[int, str, float, datetime, bool],
    over_count: int = 1024,
    unit: str = "",
) -> Union[int, str, float, datetime]:
    """
    コンソール入力処理

    Parameters
    ----------
    print_str : str
        表示文字列
    type : Union[int, str, float, datetime]
        出力タイプ
    over_count : int
        オーバーフロー回数 by default 1024
    unit : str
        単位 by default ""

    Returns
    -------
    Union[int, str, float]
        入力されたデータ

    Raises
    ------
    TypeError
        予期しないタイプ
    OverflowError
        無限ループ対策
    """
    result: Union[int, str, float, datetime, bool]
    if unit:
        unit = f"[{unit}]"
    for _ in range(over_count):
        try:
            if type == bool:
                data = input(print_str + "入力[Yn]:")
                if data.lower() == "y":
                    result = True
                elif data.lower() == "n":
                    result = False
                else:
                    raise ValueError
                if result:
                    if input("Y? [Yn]:").lower() == "y":
                        break
                else:
                    if input("n? [Yn]:").lower() == "y":
                        break
            else:
                data = input(print_str + f"入力{unit}:")
                if type == int:
                    result = int(data)
                elif type == float:
                    result = float(data)
                elif type == str:
                    result = data
                elif type == datetime:
                    result = datetime.strptime(data, "%M:%S")
                else:
                    raise TypeError
                if input(data + "? [Yn]:").lower() == "y":
                    break
        except ValueError:
            pass
    else:
        raise OverflowError
    return result
