<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Problem Statement</h1>
    <hr>
     <p> Designing databases for storing, processing, and analyzing pricing data. Data are taken from here:<a href="https://www.cryptodatadownload.com/data/binance/">Click here</a></p>
    <h2>Final approach</h2>
    csv files (pricing data ) are downloaded through web scraping, after which they are cleaned
    using pandas. Data are going to be distributed across several databases.
         For example, we create a database with only BTC pricing data, EOS pricing data, ETH pricing data, and LTC pricing data.
  <ul>  
      Input required:  </li>
      <li>BTCUSDT_Binance_futures_data_day.csv</li>
      <li>EOSUSDT_Binance_futures_data_day</li>
      <li>ETHUSDT_Binance_futures_data_day</li>
      <li>LTCUSDT_Binance_futures_data_day</li>
      <li>TO DO: Add Entity relationship model </li>

  </ul>
     <h2>Pseudo Code</h2>
   <ul>
     <li>Step 1: Download csv files through web scraping</li>
     <li>Step 2: Clean and store data in a mysql database</li>
     <li>Step 3: Create new two tables: closingPrice and OpeningPrice. 
        Define relationships between tables</li>
     <li>Step 4: Analyze closingPrice table</li>
   </ul>     
     <h2>Codes</h2>
    <ul>
        <li>analysis.py -> data visualization </li>
        <li>Load2mysql.py -> populate a mysql database with pricing data from each csv file</li>
        <li>scraper.py -> downloads pricing data from <a href="https://www.cryptodatadownload.com/data/binance/">Click here</a> </li>
        <li>createClosingPrice.sql -> define relationships between tables.Insert data into the closingPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
        <li>createOpeningPrice.sql -> define relationships between tables. Insert data into the OpeningPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
    </ul>

</body>


