import pandas
from scipy.stats import shapiro
from scipy.stats import kstest, norm
from mysticML.utils import Daddy
import warnings

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
    n = self.x.shape[0]
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

        with warnings.catch_warnings():
          warnings.simplefilter("ignore")
          stat, p_value_s = shapiro(t)

        kstest_result = kstest(t, norm.cdf)
        ks_statistic, p_value_k = kstest_result
        if n > 5000:
          if p_value_k > 0.05 and flag == 0:
            self.x[col].fillna(self.x[col].mean(), inplace=True)
          else:
            self.x[col].fillna(self.x[col].median(), inplace=True)
        else:
          if p_value_s > 0.05 and flag == 0:
            self.x[col].fillna(self.x[col].mean(), inplace=True)
          else:
            self.x[col].fillna(self.x[col].median(), inplace=True)
    return self.x