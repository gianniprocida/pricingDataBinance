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
   
    return cnx


def data_cleaning(filename):
    """ Cleans a csv files by :
        1)Loading the filename as a Pandas Dataframe.
        2)Dropping Nan values from the Pandas Dataframe,
        3)splitting the values in the 'date' column into two columns, 'date' and 'time', using a space character as the separator,
        4)converting the values in the "date" column of from string format to datetime format,
        5)droping 'time' and 'tradecount' columns,
        6)renaming 'Volume crypto' and 'Volume USDT' into 'Volume_crypto' and 'Volume_USDT',
        7)setting the 'ii' column as index
        

        Args:
        filename (csv file) : File to be preprocessed 
        
        Returns:
        clean_df DataFrame : Pandas Dataframe

        Raises:
          Error: If the filename does not exist

    """
    
    if not os.path.isfile(filename):
        raise Exception("File dos not exist")

    dataset = pd.read_csv(filename, sep = ',', decimal=',',skiprows=1)
    print(f"Preprocessing for file {filename} started ..")
    dataset.dropna(inplace=True)
    dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)
    dataset["date"] = pd.to_datetime(dataset["date"], infer_datetime_format=True)
    clean_df = dataset.drop(columns=['time', 'tradecount'])
    clean_df.rename(columns={clean_df.columns[7]:"Volume_crypto"},inplace=True)
    clean_df.rename(columns={clean_df.columns[8]: "Volume_USDT"},inplace=True)
    clean_df['symbol'] = clean_df['symbol'].str.replace('/','')
    clean_df.drop(['unix'], axis = 1, inplace = True) 
    ii = []
    # Adding an artificial index
    for i in range(clean_df.shape[0]):
       ii.append(i)
    clean_df['id'] = ii
    clean_df = clean_df.reset_index()
    clean_df.index = clean_df.index.rename('id')
    print("Finished")
    print(" ")
    return clean_df



def select_nrows(dataframe):
    """ Select the first 1020 rows from a Pandas Dataframe.

        Args:
        dataframe: (Pandas Dataframe): The input Dataframe to be sliced
        
        Returns:
        dataframe: pandas.Dataframe

         A new DataFrame containing the first n rows of the input DataFrame.


    """
    n = 1020
    return dataframe.iloc[0:n]


def createTable(cnx,dataframe,symbol,mydb):
    """ Creates a table in the 'mydb' database using a cursor object

        Args:
        cnx : A MySQL connection object.

        symbol (str) : The name of the table to be created
        
        dataframe (Pandas Dataframe): The dataframe to be used for the sql table

        mydb (str) : The name of the database to be used

        Returns:
        This function does not return anything


    """

    cur = cnx.cursor()

    cur.execute(f"""use {mydb}""")
    
    # Create an engine to connect to the database that is a string representing the database connection
    engine = create_engine("""mysql+mysqlconnector://{user}:{password}@{host}/{db}""".
    format(user="root",host="localhost",password="Chimica90$",db=mydb))
    
    createTable = f"""create table if not exists {symbol} (Date date, open decimal(12,4), 
        high decimal(12,4), low decimal(12,4), close decimal(12,4), Volume_crypto decimal(12,4), Volume_USDT decimal(12,4), 
        tradecount int not null, id int not null);"""
    
    cur.execute(createTable)


    dataframe.to_sql(con=engine, name=symbol,if_exists="replace",index=False)
  
    
    #Set 'Date' as the primary key (ideally you would want to set a composite key(id,Date), yet 
    # just leave it as it is for the time being)
    alter_table = f"""alter table {symbol} add primary key (Date);"""

    cur.execute(alter_table)
    
    cur.close()
       
    cnx.commit()





if __name__=='__main__':

   
    cnx = getConn()

    mydb = input("Enter the database you wish to create")

    cur = cnx.cursor()
    createdb = f"""create database if not exists {mydb}"""
    cur.execute(createdb)

    # cur.execute(createdb)

    # usedb = """use Cryptocurrencies"""

    # i.e. BTCUSDT, EOSUSDT, ETHUSD, LTCUSDT

    dataframes = []
    symbols = []
    for i in range(4):
        pattern = "USDT_Binance_futures_data_day.csv"
        symbol = input("Enter the symbol")
        print(f"{symbol} was entered")
        symbols.append(symbol)
        myfile = symbol + pattern
        dataframes.append(data_cleaning(myfile))

    dataframes = list(map(select_nrows,dataframes))

    while len(dataframes) > 0 and len(symbols) > 0:
        createTable(cnx,dataframes.pop(),symbols.pop(),mydb)






    
    #csv_files = [file for file in os.listdir(os.getcwd()) if
    #             file.endswith('.csv')]
    
    # Reformat datasets and get symbols for each dataset
   # output = list(map(data_cleaning, csv_files))
    
    #dataframes = [item[0] for item in output]  
   # my = dataframes[0]
   # symbols = [item[1] for item in output]

  

    # dataframes = list(map(selectNRowsfromdf,dataframes))

    
    # # Create as many as the number of csv files 
    
    
    # To run the sql script from python (TO DO)
    #https://stackoverflow.com/questions/59848116/how-to-execute-a-sql-file-using-mysql-connector-and-save-it-in-a-database-in-py

