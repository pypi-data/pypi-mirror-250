"""
@Author: kang.yang
@Date: 2024/1/11 15:57
"""
import pandas as pd


class CSV(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_all(self):
        df = pd.read_csv(self.file_name)
        res = df.values.tolist()
        return res

    def read_row_index(self, row_index: int):
        """
        index: 第一行（index=0）需要有标题，默认会忽略，取值从1开始
        """
        df = pd.read_csv(self.file_name)
        res = df.values[row_index-1].tolist()
        return res

    def read_col_index(self, col_index: int):
        """
        index：从1开始
        """
        df = pd.read_csv(self.file_name, usecols=[col_index-1])
        res = [r[0] for r in df.values.tolist()]
        return res

    def read_col_name(self, col_name: str):
        df = pd.read_csv(self.file_name, usecols=[col_name])
        res = [r[0] for r in df.values.tolist()]
        return res

    def write(self, data: dict, append=False):
        """
        :param data:
        数据格式：{
            '标题列1': ['张三', '李四'],
            '标题列2': [80, 90]
        }
        :param append: 是否追加，默认覆盖
        """
        df = pd.DataFrame(data)
        if append:
            _df = pd.read_csv(self.file_name)
            df = _df.append(df)
        df.to_csv(self.file_name, index=False)


if __name__ == '__main__':
    csv = CSV('2.csv')
    _data = {
        '标题': [1, 2, 3]
    }
    csv.write(_data)
    print(csv.read_all())

