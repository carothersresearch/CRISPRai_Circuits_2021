from lmfit import Parameters, Parameter
import numpy as np

class Params(Parameters):
    def __init__(self):
        super().__init__()
        self.exclude = []
        self.upperb = np.array([])
        self.lowerb = np.array([])

    def _getExclude(self, exclude):
        if exclude: excluded = self.exclude
        elif not exclude: excluded = []
        return excluded

    def _evalBounds(self, exclude = True):
        excluded = self._getExclude(exclude)
        self.upperb = np.array([self[i].max for i in self.__iter__() if i not in excluded])
        self.lowerb = np.array([self[i].min for i in self.__iter__() if i not in excluded])

    def _normalize(self, exclude = True):
        return (self.getValues(exclude) - self.lowerb) / (self.upperb - self.lowerb)

    def setExcluded(self, to_exclude:list):
        self.exclude = to_exclude
        self._evalBounds()

    def getValues(self, exclude = True):
        excluded = self._getExclude(exclude)
        return np.array([v.value for v in self.values() if v.name not in excluded])

    def setValues(self, x):
        for i,k in enumerate(self.values()):
            k.value = x[i]

    def getNormalizedValues(self, exclude = True):
        return self._normalize(exclude)

    def setNormalizedValues(self, x):
        for i,k in enumerate(self.values()):
            k.value = x[i]*(self.upperb[i] - self.lowerb[i])+self.lowerb[i]
            
    def makecopy(self):
        return self.__deepcopy__(None)
        
    def __deepcopy__(self, memo):
        _p = Params()
        oldP = super().__deepcopy__(memo)
        _p.__dict__.update(oldP.__dict__)
        _p.update(oldP)
        _p._evalBounds()
        return _p

    def sample(self, distribution = 'uniform', size = (1,)):
        if len(self.upperb) == 0: self._evalBounds()
            
        upperb = [self[i].max for i in self.__iter__() if self[i].vary]
        lowerb = [self[i].min for i in self.__iter__() if self[i].vary]

        if distribution == 'uniform':
            from scipy.stats import uniform
            sample = uniform.rvs(lowerb, upperb, size= size+(len(upperb),))
        elif distribution == 'log-uniform':
            from scipy.stats import loguniform
            sample = loguniform.rvs(lowerb, upperb, size= size+(len(upperb),))
        else:
            raise Error('Sampling parameters with "'+str(distribution)+'" is not implemented')
            
        if sample.shape[-1] is not len(self):
            add = np.tile([self[i].value for i in self.__iter__() if not self[i].vary],size+(1,))
            sample = np.append(sample, add, axis = -1)
            
        return sample
    
    def reorder(self,new_ordered_keys):
        _pars = Params()
        parameter_list = []
        for new_key in new_ordered_keys:
            for key, par in self.items():
                if new_key==key:
                    param = Parameter(name=par.name,
                                      value=par.value,
                                      min=par.min,
                                      max=par.max)
                    param.vary = par.vary
                    param.brute_step = par.brute_step
                    param.stderr = par.stderr
                    param.correl = par.correl
                    param.init_value = par.init_value
                    param.expr = par.expr
                    param.user_data = par.user_data
                    parameter_list.append(param)

        _pars.add_many(*parameter_list)
            
        return _pars
    def transformBounds(self, fun):
        for i in self.__iter__():
            self[i].max = fun(self[i].max)
            self[i].min = fun(self[i].min)
            
    def checkBounds(self,x):
        return np.all([self.upperb[i] > v and v > self.lowerb[i] for i,v in enumerate(x)])