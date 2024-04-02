def find_indices_of_value(value, lst):
    """
    在给定列表中找到特定值的所有索引。

    参数：
        value: 要查找的值。
        lst: 包含要搜索值的列表。

    返回：
        包含所有找到的索引的列表。
    """
    indices = [index for index, v in enumerate(lst) if v == value]
    return indices


