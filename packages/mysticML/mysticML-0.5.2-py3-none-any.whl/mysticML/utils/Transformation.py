import pandas
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.stats import shapiro
from scipy.stats import kstest, norm
from mysticML.utils import Daddy
import warnings

class Transformation(Daddy):
    def __init__(self, x: pandas.DataFrame,target:str=None,**kwargs) ->None:
        super().__init__(x, target, **kwargs)

    def check(self) ->bool:
        if not self.transform:
            return False
        numerical_cols = self.x.select_dtypes(include=[float, int]).columns
        return any(col in numerical_cols for col in self.x.columns)

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x, self.y],axis=1)
        self.report_.append("Transformation")
        for col in self.x.select_dtypes(include=[float, int]).columns:
            n = self.x.shape[0]

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                stat, p_value_s = shapiro(self.x[col])

            kstest_result = kstest(self.x[col], norm.cdf)
            ks_statistic, p_value_k = kstest_result
            if n > 5000:
                if p_value_k > 0.05:
                    scaler = StandardScaler()
                else:
                    scaler = MinMaxScaler()
            else:
                if p_value_s > 0.05:
                    scaler = StandardScaler()
                else:
                    scaler = MinMaxScaler()
            transformed_col = scaler.fit_transform(self.x[[col]])
            self.x[col] = transformed_col.flatten()
        return pandas.concat([self.x, self.y],axis=1)
