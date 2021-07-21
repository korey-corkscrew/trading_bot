import sqlite3
from pandas import read_sql_query, read_sql_table
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.series import Series
import time
from datetime import datetime
plt.close("all")

utcOffset = -18000


con = sqlite3.connect('AuguryV4.db')
cur = con.cursor()
convert = {'date' : float}
df = pd.read_sql_query(
    '''SELECT * FROM data 
    WHERE tokenAddress=\"0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619\" 
    ORDER BY date desc''', con)
df = df.astype(convert)
df['date'] =  pd.to_datetime(df['date'], unit='s')

#print(df.tokenAddress[0])
plt.figure()
date = df["date"]
price = df["tokenPrice_Quickswap"]
#ts = Series(price, index=df['date'])
#ts.plot()
plt.plot(date, price)
plt.xticks(rotation=90)
#plt.xlim(left='2021-07-17 00:00:00.0', right='2021-07-17 12:00:00.0')
plt.show()
#df.plot()
#plt.show()
#df.plot.bar()
#print(df["date"].iloc[-1])
#print(datetime.timestamp('2021-07-17 00:00:00.0'))



# Token price falls below sell stop price
'''
cursor = cur.execute('SELECT date, tokenPrice_Quickswap from data WHERE tokenAddress="0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270" ORDER by date DESC')
currPrice = cursor.fetchone()
con.close()
#print(currPrice)
#data=pd.read_sql_query("SELECT * FROM Reviews",con)
'''