from mysticML.utils import Daddy
import pandas
import numpy as np
from sklearn.utils import resample

class Sampling(Daddy):
    def __init__(self, x:pandas.DataFrame, target:str=None,**kwargs):
        super().__init__(x, target, **kwargs)
        self.col_bool = []
        self.val = {}
        self.lth = None
        self.rth = None

    def check(self) ->bool:
        if not self.sampling:
            return False
        for c,d in zip(self.y.value_counts().index.to_list(),self.y.value_counts()):
            self.val[c]=d
        mean = np.round(np.mean(list(self.val.values())))
        self.lth = round(mean - 0.2 * mean)
        self.rth = round(mean + 0.2 * mean)
        for i in self.val.values():
            if i<self.lth or i>self.rth:
                self.col_bool.append(True)
            else:
                self.col_bool.append(False)
        return any(self.col_bool)

    def apply(self) ->pandas.DataFrame:
        if self.check():
            self.report_.append("Sampling")
            df = pandas.DataFrame()
            c = -1
            for i in self.col_bool:
                c+=1
                if i:
                    d = self.preD(c)
                    samples = round((((list(self.val.values())[c]-min(self.val.values()))*(self.rth-self.lth))
                                                /(max(self.val.values())-min(self.val.values())))+self.lth)
                    d = resample(d, n_samples=samples)
                    df = pandas.concat([df,d])
                else:
                    df = pandas.concat([df,self.preD(c)])
            return df
        else:
            return pandas.concat([self.x, self.y],axis=1)

    def preD(self, c:int) ->pandas.DataFrame:
        d = self.x.copy()
        d[self.target] = self.y[self.y==list(self.val.keys())[c]]
        d.dropna(inplace=True)
        return d
