from dataclasses import replace
from symtable import Symbol
from nsetools import Nse
import pandas as pd
import numpy as np
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from google import Create_Service
import csv
# historical trend
from nsepy import get_history
from datetime import datetime
from datetime import datetime, timedelta
today = datetime.today().date()
thirty_days_ago = today - timedelta(days=30)

nse = Nse()
tmp = []
hst = []
symbol = ['LTI','LTTS','DMART','KPITTECH','OLECTRA','LICI','TEGA','LATENTVIEW','TATAPOWER','INDOCO']
for x in symbol:
    q = nse.get_quote(x)# it's ok to use both upper or lower case for codes.
    columns = list(q.keys())
    values = list(q.values())
    arr_len = len(values)
    df_q = pd.DataFrame(np.array(values, dtype=object).reshape(1, arr_len), columns=columns)
    tmp.append(df_q)
    hdata = get_history(symbol = x,start=thirty_days_ago,end=today)
    hst.append(hdata)
df = pd.concat(tmp)
df1 = pd.DataFrame(df)
df2 = df1.loc[ :, ['pricebandupper',
'symbol',
'applicableMargin',
'totalSellQuantity',
'companyName',
'marketType',
'css_status_desc',
'dayHigh',
'basePrice',
'securityVar',
'pricebandlower',
'sellQuantity5',
'sellQuantity4',
'sellQuantity3',
'cm_adj_high_dt',
'sellQuantity2',
'dayLow',
'sellQuantity1',
'quantityTraded',
'pChange',
'totalTradedValue',
'deliveryToTradedQuantity',
'totalBuyQuantity',
'averagePrice',
'cm_ffm',
'buyPrice2',
'secDate',
'buyPrice1',
'high52',
'previousClose',
'low52',
'buyPrice4',
'buyPrice3',
'deliveryQuantity',
'buyPrice5',
'extremeLossMargin',
'cm_adj_low_dt',
'varMargin',
'sellPrice1',
'sellPrice2',
'totalTradedVolume',
'sellPrice3',
'sellPrice4',
'sellPrice5',
'change',
'buyQuantity4',
'isExDateFlag',
'buyQuantity3',
'buyQuantity2',
'buyQuantity1',
'series',
'faceValue',
'buyQuantity5',
'closePrice',
'open',
'isinCode',
'lastPrice']]

gc = gspread.service_account(filename='modular-skyline-353602-05178b341f8f.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1eiKgQsvmnKkowwp0TPzQgace4kIpxkZ7b6Y4etS_Z3Q')
ws = sh.get_worksheet(1)
set_with_dataframe(ws,df2)

# historical trend
hst_df = pd.concat(hst)
hst_df1 = pd.DataFrame(hst_df)
ws = sh.get_worksheet(2)
set_with_dataframe(ws,hst_df1)