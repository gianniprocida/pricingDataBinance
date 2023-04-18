import os
import pandas as pd
from Load2mysql import getConn
import matplotlib.pyplot as plt



def analyzeclosingprice():
    cnx = getConn()

    cur = cnx.cursor()

    cur.execute("use pricingdata")

    df = pd.read_sql("select * from closingprice",cnx)

    df.set_index('Date',inplace=True)


    subset1 = df.loc[:, ['BTC', 'ETH','EOS','LTC']]

    print(subset1.corr())


    # Calculation of daily percentage

    ret = subset1.pct_change()*100

    #Plotting the histogram by specifying the number of bins

    ret.hist(bins=50)

    # Box plot

    ret.plot(kind="box",figsize=(16,5))


if __name__=='__main__':
    analyzeclosingprice()
