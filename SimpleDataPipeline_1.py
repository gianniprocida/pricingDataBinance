import pandas as pd
import os
import mysql.connector
from sqlalchemy import create_engine
import time
from uploadtoSlack import *


headers = {
    'Authorization': 'Bearer xoxb-4383281664871-4410711262321-0FYV46aLphYmzR7OkMd56795',
    'Content-Type': 'application/x-www-form-urlencoded'
}
url = "https://slack.com/api/files.upload"


def getConn():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chimica90$"
    )
    cur = cnx.cursor(buffered=True)
    return cnx, cur


def ReformatData(filename):
    dataset = pd.read_csv(filename, sep=',', decimal=',', skiprows=1)
    dataset.dropna(inplace=True)
    # Expand = True , It will expand 'date' and 'time' out into separate columns
    dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)
    # Converting dataset["date"] to datetime
    dataset["date"] = pd.to_datetime(
        dataset["date"], infer_datetime_format=True)
    reformatted = dataset.drop(columns=['time', 'tradecount'])
    # Replacing space with underscore
    reformatted.rename(
        columns={reformatted.columns[7]: "Volume_crypto"}, inplace=True)
    reformatted.rename(
        columns={reformatted.columns[8]: "Volume_USDT"}, inplace=True)
    symbol = filename.split('_')[0]
    reformatted['symbol'] = reformatted['symbol'].str.replace('/', '')
    return reformatted, symbol


def getMinNumOfRows(dataframes):
    minNumofRows = dataframes[0].shape[0]
    for i in dataframes:
        if i.shape[0] < minNumofRows:
            minNumofRows = i.shape[0]
    return minNumofRows


def deleteRowsAt(dataframes, minNumofRows):
    for i in dataframes:
        i.drop(i.index[minNumOfRows + 1:], axis=0, inplace=True)
    return dataframes


def createParentTable(cnx, cur, dataframe):

    tableName = "BinanceData"

    cur.execute(usedb)

    engine = create_engine("""mysql+mysqlconnector://{user}:{password}@{host}/{db}""".
                           format(user="root", host="localhost", password="Chimica90$", db="Cryptotest"))

    createTable = f"""create table if not exists {tableName} (unix int not null, Date date, open decimal(12,4), 
        high decimal(12,4), low decimal(12,4), close decimal(12,4), Volume_crypto decimal(12,4), Volume_USDT decimal(12,4), 
        tradecount int not null)"""

    cur.execute(createTable)

    dataframe.to_sql(con=engine, name=tableName,
                     if_exists="replace", index=True)

    cnx.commit()
    return cnx


def appendToParentTable(cnx, cur, dataframe):

    tableName = "BinanceData"
    engine = create_engine("""mysql+mysqlconnector://{user}:{password}@{host}/{db}""".
                           format(user="root", host="localhost", password="Chimica90$", db="Cryptotest"))

    dataframe.to_sql(con=engine, name=tableName,
                     if_exists="append", index=True)

    cnx.commit()


def createChildTable(cnx, cur):
    createTablewithClosingPrice = """create table if not exists ClosingPrice as select Date from BinanceData 
    where BinanceData.index between 0 and 900;"""

    cur.execute(createTablewithClosingPrice)

    cnx.commit()


def populateChildTable(cnx, cur, symbols):

    while len(symbols) > 0:

        symb = symbols.pop()

        alterTablewithClosingPrice = f"""alter table ClosingPrice add column {symb} decimal(12,4) after Date"""

        cur.execute(alterTablewithClosingPrice)

        print("Inserting {} closing price into ClosingPrice table...".format(symb))
        print(" ")

        updateTablewithClosingPrice = f"""update ClosingPrice inner join BinanceData 
       on ClosingPrice.Date = BinanceData.Date and BinanceData.symbol='{symb}'
       set ClosingPrice.{symb} = BinanceData.close"""

        print(updateTablewithClosingPrice)
        cur.execute(updateTablewithClosingPrice)
        cnx.commit()
        time.sleep(5)


if __name__ == '__main__':

    (cnx, cur) = getConn()

    createdb = """create database if not exists Cryptotest"""

    cur.execute(createdb)

    usedb = """use Cryptotest"""

    csv_files = [file for file in os.listdir(os.getcwd()) if
                 file.endswith('.csv')]

    # Reformat datasets and get symbols for each dataset
    output = list(map(ReformatData, csv_files))

    dataframes = [item[0] for item in output]

    symbols = [item[1] for item in output]

    # I want my dataframes to have the same number of rows
    minNumOfRows = getMinNumOfRows(dataframes)

    dataframes = deleteRowsAt(dataframes, minNumOfRows)

    ##  Uploading dataframes to slack

    fileobjs = list(map(csv2fileobj, dataframes))

    urls = uploadFiles(fileobjs, symbols)


    # Create ParentTable (single table containing data from one dataframe)
    onedataframe = dataframes.pop()

    cnx = createParentTable(cnx,cur,onedataframe)

    # Add the rest of dataframes
    while len(dataframes) > 0:
        appendToParentTable(cnx,cur,dataframes.pop())

    # Create childTable ( table with closing price per each dataframe)
    createChildTable(cnx,cur)
    populateChildTable(cnx,cur,symbols)
