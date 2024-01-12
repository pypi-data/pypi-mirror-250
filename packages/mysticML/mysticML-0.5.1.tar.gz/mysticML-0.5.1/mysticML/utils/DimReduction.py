from mysticML.utils import Daddy
import pandas
from sklearn.decomposition import PCA
from math import ceil
pandas.options.mode.chained_assignment=None

class DimReduction(Daddy):

    def __init__(self,x:pandas.DataFrame, target:str=None, **kwargs)->None:
        super().__init__(x, target, **kwargs)
        self.pca = None

    def check(self) ->bool:
        if not self.dim_red:
            return False
        s = self.x.shape[1]
        if s > 5:
            self.pca = PCA(n_components=ceil(s/2))
            return True
        return False

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x, self.y], axis=1)
        self.report_.append("DimRed")
        columns = ['pca_comp_%i' % i for i in range(ceil(self.x.shape[1]/2))]
        x = pandas.DataFrame(self.pca.fit(self.x).transform(self.x), columns=columns)
        return pandas.concat([x, self.y], axis=1)
