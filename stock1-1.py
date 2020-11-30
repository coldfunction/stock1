import io
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use('ggplot')


import requests
import pandas as pd
import json
import numpy as np



def crawl_price(stock_id):

    #d = datetime.datetime.now()
    #url = "https://query1.finance.yahoo.com/v8/finance/chart/"+stock_id+"?period1=0&period2="+str(int(d.timestamp()))+"&interval=1d&events=history&=hP2rOschxO0"

    #res = requests.get(url)
   # data = json.loads(res.text)
    #df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
   # return df
  
    now = int(datetime.datetime.now().timestamp())+86400
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"

    #print(url)

    #return url
    response = requests.get(url)


    f = io.StringIO(response.text)
    df = pd.read_csv(f, index_col='Date', parse_dates=['Date'] )

    return df



#ts = time.time()
#current_t = int(ts)
#site = ""

#台積電 2330.TW
#特斯拉 TSLA
#twii = crawl_price("^TWII")
#twii.head()

#mean = twii['close'].pct_change().rolling(252).mean()
#std = twii['close'].pct_change().rolling(252).std()

#sharpe = mean / std

#twii.close.plot()
#sharpe.plot(secondary_y=True)

def backtest(twii, sharpe, a, b, c, d, days_ago, e):
    sr = sharpe
    srsma = sr.rolling(a).mean()

    srsmadiff = srsma.diff() * 100
    ub = srsmadiff.quantile(b)
    lb = srsmadiff.quantile(c)
    
    buy = ((srsmadiff.shift(d) < lb) & (srsmadiff > ub))
    sell = ((srsmadiff.shift(d) > ub) & (srsmadiff < lb))

    hold = pd.Series(np.nan, index=buy.index)
    hold[buy] = 1
    hold[sell] = 0

    hold.ffill(inplace=True)
    
    adj = twii['Adj Close'][buy.index]

    if e == 1 :
        #eq = (adj.pct_change().shift(-1)+1).fillna(1)[hold == 1].cumprod().plot(xlim=[pd.Timestamp('2020-02-15'), pd.Timestamp('2020-09-09')])
        #hold.plot(xlim=[pd.Timestamp('2020-02-15'), pd.Timestamp('2020-09-09')])
#(datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        #eq = (adj.pct_change().shift(-1)+1).fillna(1)[hold == 1].cumprod().plot(xlim=[pd.Timestamp((datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")), pd.Timestamp(datetime.datetime.now().strftime("%Y-%m-%d"))])
        #hold.plot(xlim=[pd.Timestamp((datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")), datetime.datetime.now().strftime("%Y-%m-%d")])
        eq = (adj.pct_change().shift(-1)+1).fillna(1)[hold == 1].cumprod().plot(xlim=[pd.Timestamp((datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")), (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")  ])
        hold.plot(xlim=[pd.Timestamp((datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")), (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d") ])
    if e == 2 :
        hold.plot(xlim=[pd.Timestamp((datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")), (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d") ])



        #eq = (adj.pct_change().shift(-1)+1).fillna(1)[hold == 1].cumprod().plot()
        #hold.plot()

    eq = (adj.pct_change().shift(-1)+1).fillna(1)[hold == 1].cumprod()
    if len(eq) > 0:
        return eq.iloc[-1]
    else:
        return 1

#backtest(252,0.4,0.6,4,1)

def find_opt(twii, sharpe):

    list={}
    maxeq = 0

    for a in range(100,200,20):
        for b in np.arange(0.3, 0.9, 0.03):
            for c in np.arange(0.3, 0.6, 0.03):
                for d in range(60, 180, 10):
                
                    eq = backtest(twii, sharpe, a,b,c,d,60, 0)
                
                    if maxeq < eq:
                        maxeq = eq
                        print(eq, a,b,c,d)
                        list[0]=eq
                        list[1]=a
                        list[2]=b
                        list[3]=c
                        list[4]=d
    return list
#list = find_opt()


def showMe_best_sp(stock_id):
    twii = crawl_price(stock_id)
    twii.head()

    mean = twii['Adj Close'].pct_change().rolling(252).mean()
    std = twii['Adj Close'].pct_change().rolling(252).std()

    sharpe = mean / std


    list = find_opt(twii, sharpe)

    backtest(twii, sharpe, list[1],list[2],list[3],list[4],60,2)
    return sharpe, twii


