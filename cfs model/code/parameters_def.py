# File with all default parameters
from utils import Params

w = 100
kt1 = 0.06*0.006    # TX and TL
kt2 = 0.06/1000*25    # TX
kt0 = kt1/10            # leak
ka =  0.06/1000*13
ki =  0.06/1000*20
caskon =  0.06/1000*20
kta1 = 6*kt1
kta2 = 6*0.06/1000
kdeg = 6.6/8000
kmat= 3e-4

def main():
    small_model_p = Params()
    small_model_p.add('ktC', kt1, min = kt1/w, max = kt1*w)
    small_model_p.add('ktS', kt1, min = kt1/w, max = kt1*w)
    small_model_p.add('ktR0', kt0, min = kt0/w, max = kt0*w)
    small_model_p.add('ktg10', kt2, min = kt2/w, max = kt2*w)
    small_model_p.add('ktg20', kt2, min = kt2/w, max = kt2*w)
    small_model_p.add('ka', ka, min = ka/w, max = ka*w)
    small_model_p.add('ki', ki, min = ki/w, max = ki*w)
    small_model_p.add('ktR1', kta1, min = kta1/w, max = kta1*w)
    small_model_p.add('ktg21', kta2, min = kta2/w, max = kta2*w)
    small_model_p.add('caskon', caskon, min = caskon/w, max = caskon*w)
    small_model_p.add('kdeg', kdeg, min = kdeg/w, max = kdeg*w)
    
    large_model_p = Params()
    large_model_p.add('ktx1', kt1, min = kt1/w, max = kt1*w, vary = True)
    large_model_p.add('ktx2', kt2, min = kt2/w, max = kt2*w, vary = True)
    large_model_p.add('ktx01', kt0, min = kt0/w, max = kt0*w, vary = True)
    large_model_p.add('ktx02', kt0, min = kt0/w, max = kt0*w, vary = True)
    large_model_p.add('kmat3', kmat, min = kmat/w, max = kmat*w, vary = True)
    large_model_p.add('kmat2', kmat, min = kmat/w, max = kmat*w, vary = True)
    large_model_p.add('kmat1', kmat, min = kmat/w, max = kmat*w, vary = True)
    large_model_p.add('kdeg', kdeg, min = kdeg/w, max = kdeg*w,vary = True)
    large_model_p.add('ka', ka, min = ka/w, max = ka*w)
    large_model_p.add('ki', ki, min = ki/w, max = ki*w)
    large_model_p.add('caskon', caskon, min = caskon/w, max = caskon*w)
    large_model_p.add('kta1', kta1, min = kta1/w, max = kta1*w)
    large_model_p.add('kta2', kta2, min = kta2/w, max = kta2*w)



    return {'small_model_p':small_model_p,'large_model_p':large_model_p}