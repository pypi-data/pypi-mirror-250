import pandas
from scipy.stats import shapiro
from mysticML.utils import Daddy

class Imputation(Daddy):
  def __init__(self, x: pandas.DataFrame, target:str=None,**kwargs) -> None:
    super().__init__(x, target, **kwargs)
    self.x = pandas.concat([self.x,self.y],axis=1)

  def check(self) -> bool:
    if not self.impute:
      return False
    si = self.x.shape[0]
    temp = self.x.dropna()
    sf = temp.shape[0]
    if si == sf:
      return False
    else:
      return True

  def apply(self) -> pandas.DataFrame:
    if not self.check():
      return self.x
    self.report_.append("Imputation")
    flag=0
    null_per = self.x.isnull().mean()
    col_drop = null_per[null_per > 0.6].index
    assert self.target not in col_drop, f"{self.target} is filled mostly with null values ; cannot be a target column."
    self.x.drop(col_drop, axis=1, inplace=True)
    self.x.dropna(subset=[self.target],axis=0,inplace=True)
    rows_with_majority_nan = self.x[(self.x.isna().sum(axis=1) > (self.x.shape[1]/2)).values]
    self.x = self.x.drop(rows_with_majority_nan.index)
    rows_to_drop = self.x[self.x.isna().any(axis=1)].index
    if len(rows_to_drop) <= 0.02 * len(self.x):
      self.x.drop(rows_to_drop, inplace=True)
    for col in self.x.columns:
      if (self.x[col].dtype == 'object') or (self.x[col].dtype == 'int64' and self.x[col].nunique() <= 11 and self.x[col].min() >= 0):
        flag=1
        self.x[col].fillna(self.x[col].mode()[0],inplace=True)
      if self.x[col].dtype in [float, int]:
        t = self.x[col]
        t.dropna(inplace=True)
        stat, p_value = shapiro(t)
        if p_value > 0.05 and flag==0:
          self.x[col].fillna(self.x[col].mean(),inplace=True)
        else:
          self.x[col].fillna(self.x[col].median(),inplace=True)
    return self.x