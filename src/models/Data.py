import numpy as np
import pandas as pd


class Data:

    def __init__(self, commodities, *args) -> None:
        self.datas = commodities, *args


    @property
    def datas(self):
        return self._data


    @datas.setter
    def datas(self, value):
        if value[1:] is not None:
            # np.array(list((d1, d2, d3, d4, d5, d6, d7, d8, d9, dn))).T.tolist()
            value = list(value)
            arr = np.array(value).T
            df = pd.DataFrame(arr)
            df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x.astype('float'), axis=1)
            arr = df.values.tolist()
        else:
            arr = None
        self._data = arr


    @property
    def num_data(self):
        return len(self._data)


if __name__ == '__main__':
    d = Data(['a', 'b', 'c', 'd'], ['123', '12345', '123456', '1234567'], ['1', '2', '3', '4'])
    print('d.datas:', d.datas)
