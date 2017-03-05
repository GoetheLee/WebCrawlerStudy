import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

from matplotlib import font_manager, rc
#font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
#rc('font', family=font_name)

#%matplotlib inline

plt.rcParams['axes.unicode_minus'] = False
plt.rc('figure', figsize=(10, 6))

