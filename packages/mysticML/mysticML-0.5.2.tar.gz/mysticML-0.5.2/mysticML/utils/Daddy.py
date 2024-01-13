import pandas

class Daddy:

    report_ = []

    def __init__(self, x:pandas.DataFrame, target:str=None, combo:str='advanced',
                 duplicate: bool = None, outlier: bool = None, impute: bool = None,
                 transform: bool = None, encode: bool = None,
                 feature_sel: bool = None, dim_red: bool = None, sampling: bool = None) ->None:

        if target is not None:
            self.x = x.drop([target],axis=1)
            self.y = x[target]
            self.target = target
        else:
            self.x = x.iloc[:,:-1]
            self.y = x.iloc[:,-1]
            self.target = x.columns[-1]

        if duplicate is False:
            self.duplicate = False
        else:
            self.duplicate = True
        if outlier is False:
            self.outlier = False
        else:
            self.outlier = True
        if impute is False:
            self.impute = False
        else:
            self.impute = True
        if transform is False:
            self.transform = False
        else:
            self.transform = True
        if encode is False:
            self.encode = False
        else:
            self.encode = True
        if feature_sel is False:
            self.feature_sel = False
        else:
            self.feature_sel = True
        if dim_red is False:
            self.dim_red = False
        else:
            self.dim_red = True
        if sampling is False:
            self.sampling = False
        else:
            self.sampling = True

        assert combo in ['basic', 'intermediate', 'advanced'], f"unknown value {combo} passed " \
                                                               f"for parameter combo." \
                                                               f"\n allowed values: " \
                                                               f"['basic', 'intermediate', 'advanced']"
        self.combo = combo

        if combo == 'intermediate':
            if not feature_sel:
                self.feature_sel = False
            if not dim_red:
                self.dim_red = False
            if not sampling:
                self.sampling = False

        elif combo == 'basic':
            if not feature_sel:
                self.feature_sel = False
            if not dim_red:
                self.dim_red = False
            if not sampling:
                self.sampling = False
            if not encode:
                self.encode = False
            if not transform:
                self.transform = False

        if encode is False:
            assert feature_sel is False or feature_sel is None, "feature_sel cannot be set to True when encode is set to False."
            assert dim_red is False or dim_red is None, "dim_red cannot be set to True when encode is set to False."
            self.feature_sel = False
            self.dim_red = False

        if impute is False:
            assert sampling is False or sampling is None, "sampling cannot be set to True when imputation is set to False."
            assert feature_sel is False or feature_sel is None, "feature_sel cannot be set to True when imputation is set to False."
            assert dim_red is False or dim_red is None, "dim_red cannot be set to True when imputation is set to False."
            self.sampling = False
            self.feature_sel = False
            self.dim_red = False


    def check(self) ->bool:
        raise NotImplementedError
    def apply(self) ->pandas.DataFrame:
        raise NotImplementedError