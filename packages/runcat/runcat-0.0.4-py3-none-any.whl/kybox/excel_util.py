"""
pip install pandas==1.3.4
pip install openpyxl==3.0.9
"""
import pandas as pd


class Excel(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_sheet(self, sheet_name=0):
        df = pd.read_excel(self.file_name, sheet_name=sheet_name)
        res = df.values.tolist()
        return res

    def read_row_index(self, row_index: int, sheet_name=0):
        """
        index：第一行（index=0）需要有标题，默认会忽略，取值从1开始
        """
        df = pd.read_excel(self.file_name, sheet_name=sheet_name)
        res = df.values[row_index-1].tolist()
        return res

    def read_col_index(self, col_index: int, sheet_name=0):
        """
        index：从1开始
        """
        df = pd.read_excel(self.file_name, usecols=[col_index-1], sheet_name=sheet_name)
        res = [r[0] for r in df.values.tolist()]
        return res

    def read_col_name(self, col_name: str, sheet_name=0):
        df = pd.read_excel(self.file_name, sheet_name=sheet_name)
        res = df[col_name].values.tolist()
        return res

    def write_sheet(self, data: dict, sheet_name='sheet1', append=False):
        """
        :param data:
        数据格式：{
            '标题列1': ['张三', '李四'],
            '标题列2': [80, 90]
        }
        :param sheet_name: sheet名称
        :param append: 是否进行追加，默认覆盖
        """

        df = pd.DataFrame(data)
        if append:
            _df = pd.read_excel(self.file_name, sheet_name=sheet_name)
            df = _df.append(df)

        writer = pd.ExcelWriter(self.file_name)
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()

    def write_sheets(self, sheet_dict: dict, append=False):
        """
        :param sheet_dict:
        数据格式: {
            'sheet1_name': {'标题列1': ['张三', '李四'], '标题列2': [80, 90]},
            'sheet2_name': {'标题列3': ['王五', '郑六'], '标题列4': [100, 110]}
        }
        :param append: 是否追加，默认覆盖
        """
        df_dict = {}
        for sheet_name, sheet_data in sheet_dict.items():
            df_dict[sheet_name] = pd.DataFrame(sheet_data)

        writer = pd.ExcelWriter(self.file_name)
        for sheet_name, sheet_data in sheet_dict.items():
            _df = pd.DataFrame(sheet_data)
            if append:
                _df = df_dict[sheet_name].append(_df)
            _df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()

    def get_sheet_names(self):
        return list(pd.read_excel(self.file_name, sheet_name=None))


if __name__ == '__main__':
    excel = Excel('1.xlsx')
    print(excel.get_sheet_names())












