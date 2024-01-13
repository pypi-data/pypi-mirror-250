from mysticML.utils import Daddy
import pandas
pandas.options.mode.chained_assignment=None

class Duplicate(Daddy):
    """
        This class must run before data scaling (up-sampling).
    """
    def __init__(self, x:pandas.DataFrame, target:str=None, **kwargs) ->None:
        super().__init__(x, target, **kwargs)

    def check(self) ->bool:
        if not self.duplicate:
            return False
        return True

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x,self.y],axis=1)
        self.report_.append("Duplicate")
        self.x.drop_duplicates(inplace=True)
        return pandas.concat([self.x,self.y],axis=1)