import pandas
from scipy.stats import zscore
from mysticML.utils import Daddy


class Outlier(Daddy):
    def __init__(self, x: pandas.DataFrame, target:str=None, **kwargs) -> None:
        super().__init__(x, target, **kwargs)

    def check(self) -> bool:
        if not self.outlier:
            return False
        return any(self.x[col].dtype in [float, int] for col in self.x.columns)

    def apply(self) -> pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x, self.y], axis=1)
        self.report_.append("Outlier")
        for col in self.x.select_dtypes(include=[float, int]).columns:
            z_scores = zscore(self.x[col])
            outliers = (z_scores > 1.5) | (z_scores < -1.5)
            self.x.loc[outliers, col] = pandas.NA
        return pandas.concat([self.x, self.y], axis=1)