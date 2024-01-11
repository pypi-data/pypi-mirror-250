import pandas
from mysticML.utils import Duplicate, Outlier, \
    Imputation, Transformation, Encoding, \
    FeatureSelection, DimReduction, Sampling


class Preprocess(object):
    def __init__(self, df:pandas.DataFrame) ->None:
        self.report_ = None
        self.df = df

    def fit(self, target:str=None, combo:str='advanced',
            duplicate:bool=None, outlier:bool=None, impute:bool=None,
            transform:bool=None, encode:bool=None,
            feature_sel:bool=None, dim_red:bool=None, sampling:bool=None) ->pandas.DataFrame:

        df = self.df

        operations = [Duplicate, Outlier, Imputation,
        Transformation, Encoding, FeatureSelection, DimReduction, Sampling]

        for operation in operations:
            op = operation(df,target=target,combo=combo,duplicate=duplicate,
                           outlier=outlier,impute=impute,transform=transform,encode=encode,
                           feature_sel=feature_sel,dim_red=dim_red,sampling=sampling)
            df = op.apply()
            self.report_ = op.report_

        return df

