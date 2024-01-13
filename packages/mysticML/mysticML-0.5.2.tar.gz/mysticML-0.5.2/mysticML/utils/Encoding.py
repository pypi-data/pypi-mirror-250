import pandas
from mysticML.utils import Daddy

class Encoding(Daddy):
    def init(self, x: pandas.DataFrame, target:str=None,**kwargs) -> None:
        super().__init__(x, target, **kwargs)

    def check(self) ->bool:
        if not self.encode:
            return False
        return any(self.x[col].dtype == object for col in self.x.columns)

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x,self.y],axis=1)
        self.report_.append("Encoding")
        for col in self.x.select_dtypes(include=[object]).columns:
            d = dict(self.x[col].value_counts())
            d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
            s = sum(d.values())
            for i,j in d.items():
                d[i] = 1-j/s
            self.x[col] = self.x[col].map(d)
        return pandas.concat([self.x,self.y],axis=1)
