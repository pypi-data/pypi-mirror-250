import pandas
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.stats import shapiro
from mysticML.utils import Daddy

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
            stat, p_value = shapiro(self.x[col])
            if p_value > 0.05:
                scaler = StandardScaler()
            else:
                scaler = MinMaxScaler()
            transformed_col = scaler.fit_transform(self.x[[col]])
            self.x[col] = transformed_col.flatten()
        return pandas.concat([self.x, self.y],axis=1)
