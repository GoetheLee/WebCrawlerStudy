from pandas_datareader import data, wb
from datetime import datetime

df = data.DataReader("KRX:KOSPI", "google")
'''
df = data.DataReader(
    "KRX:KOSPI"
    "google"
    datetime(2016, 01, 01)
    datetime(2016, 12, 31)
)
'''
print (df)

ax = df.Close.plot()
ax.set_title("Kospi")
ax.set_ylabel("Index")
ax.set_xlim("2016-01-01", "2016-11-15")


