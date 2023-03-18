<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Cryptocurrency analysis</h1>
    <hr>
     <p> Relational database with pricing data extracted from : <a href="https://www.cryptodatadownload.com/data/binance/">Click here</a></p>
    <h2>Python files</h2>
  <ul>
      <li> scraper.py</li>
      <li> simpleDataPipeline</li>
  </ul>
     <h2>Other files</h2>
   <ul>
     <li> csv_files/*.csv (pricing data) </li>
   </ul>     
     <h2>Description</h2>
    <ul>
        <li>analysis.py -> data visualization </li>
        <li>Load2mysql.py -> populate a mysql database with pricing data from each csv file</li>
        <li>scraper.py -> downloads pricing data from <a href="https://www.cryptodatadownload.com/data/binance/">Click here</a> </li>
        <li>createClosingPrice.sql -> define relationships among tables.Insert data into the closingPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
        <li>createOpeningPrice.sql -> define relationships among tables. Insert data into the OpeningPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
    </ul>

</body>


