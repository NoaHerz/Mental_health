# Compare models :
from scipy import stats

def lrtest(llmin, llmax,df = 1):
    lr = 2 * (llmax - llmin)
    if llmax<llmin:
        raise ValueError('Check assumptions.')
    stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
    p = stats.chisqprob(lr, df) 
    return lr, p
