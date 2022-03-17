import numpy as np
import pandas as pd

#import. The CMLReader class is your gateway to all experimental data, including electrodes and EEG. The get_data_index function specifically loads experimental databases. 
from cmlreaders import CMLReader, get_data_index

import pickle
import os
import pandas as pd
import numpy as np
import scipy.signal
from scipy.stats import zscore
from cmlreaders import CMLReader, get_data_index
from pylab import *
from correctEEGoffset import *
from convertMstoWindowNumber import convertMstoWindowNumber

import statsmodels.api as sm
from scipy import stats

import gensim.models as models
from scipy import spatial
from scipy.io import loadmat
from scipy.stats import sem
import os, csv, numpy, pandas
import pandas as pd
import numpy as np
from sklearn import preprocessing
import seaborn as sns

from statsmodels.stats.anova import AnovaRM
from lrtest import lrtest

from ptsa.data.filters import ButterworthFilter
from ptsa.data.filters import MorletWaveletFilter
from regionalizationModule import get_elec_regions,Loc2PairsTranslation
import xarray as xr
from getMTLregions import getMTLregions