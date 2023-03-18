import pandas as pd
import os
import mysql.connector
from sqlalchemy import create_engine
import time

def getConn():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chimica90$"
    )
    cur = cnx.cursor(buffered=True)
    return cnx, cur


def ReformatData(filename):
    dataset = pd.read_csv(filename, sep = ',', decimal=',',skiprows=1)
    dataset.dropna(inplace=True)
    # Expand = True , It will expand 'date' and 'time' out into separate columns
    dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)
    # Converting dataset["date"] to datetime
    dataset["date"] = pd.to_datetime(dataset["date"], infer_datetime_format=True)
    reformatted = dataset.drop(columns=['time', 'tradecount'])
    # Replacing space with underscore 
    reformatted.rename(columns={reformatted.columns[7]:"Volume_crypto"},inplace=True)
    reformatted.rename(columns={reformatted.columns[8]: "Volume_USDT"},inplace=True)
    symbol = filename.split('_')[0]
    reformatted['symbol'] = reformatted['symbol'].str.replace('/','')
    reformatted.drop(['unix'], axis = 1, inplace = True) 
    ii = []
    for i in range(reformatted.shape[0],0,-1):
       ii.append(i)
    reformatted['id'] = ii
    reformatted = reformatted.reset_index()
    reformatted.index = reformatted.index.rename('id')
    return reformatted,symbol


def getMinNumOfRows(dataframes):
    minNumofRows = dataframes[0].shape[0]
    for i in dataframes:
        if i.shape[0] < minNumofRows:
            minNumofRows = i.shape[0]
    return minNumofRows


# csv files have different number of rows so using this function there will be no risk of
# having dataframes with different n of rows
def selectNRowsfromdf(dataframe):
    n = 1030
    return dataframe.iloc[0:n]


def createTable(dataframe,symbol):
 
    cur.execute(usedb)
    
    engine = create_engine("""mysql+mysqlconnector://{user}:{password}@{host}/{db}""".
    format(user="root",host="localhost",password="Chimica90$",db="Cryptocurrencies"))
    
    createTable = f"""create table if not exists {symbol} (Date date, open decimal(12,4), 
        high decimal(12,4), low decimal(12,4), close decimal(12,4), Volume_crypto decimal(12,4), Volume_USDT decimal(12,4), 
        tradecount int not null, id int not null);"""
    
    cur.execute(createTable)


    cur.execute(f"""show columns from {symbol}""")

    dataframe.to_sql(con=engine, name=symbol,if_exists="replace",index=False)
  
    
    #Set 'Date' as primary key (ideally you would want to set a composite key(id,Date), yet 
    # just leave it as it is for the time being)
    alter_table = f"""alter table {symbol} add primary key (Date);"""

    cur.execute(alter_table)

       
    cnx.commit()
    return cnx





if __name__=='__main__':

    # Run the script only if the database doesn't exist
    # (Need to fix this, )
    (cnx, cur) = getConn()

    createdb = """create database if not exists Cryptocurrencies"""

    cur.execute(createdb)

    usedb = """use Cryptocurrencies"""


    csv_files = [file for file in os.listdir(os.getcwd()) if
                 file.endswith('.csv')]
    
    # Reformat datasets and get symbols for each dataset
    output = list(map(ReformatData, csv_files))
    
    dataframes = [item[0] for item in output]  
   # my = dataframes[0]
    symbols = [item[1] for item in output]

  

    dataframes = list(map(selectNRowsfromdf,dataframes))

    
    # Create as many as the number of csv files 
    while len(dataframes) > 0 and len(symbols) > 0:
      createTable(dataframes.pop(),symbols.pop())
    
    # To run the sql script from python (TO DO)
    #https://stackoverflow.com/questions/59848116/how-to-execute-a-sql-file-using-mysql-connector-and-save-it-in-a-database-in-py

