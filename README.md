<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Overview</h1>
    <hr>
     <p> This is a series of Python and SQL scripts that allows you to design databases for storing, processing, and analyzing pricing data. Data are taken from here:<a href="https://www.cryptodatadownload.com/data/binance/">Click here</a></p>
    <h2>Getting started</h2>
    Before using the scripts App make sure you have Python3 installed on your computer.
    csv files (pricing data ) are downloaded through web scraping, after which they are cleaned using 
    using pandas. Data are going to be distributed across several databases.
         For example, we create a database with only BTC pricing data, EOS pricing data, ETH pricing data, and LTC pricing data.

     <h3>How to run it?</h3>
   <ul>
     <li>Clone the repository from GitHub: git clone https://github.com/gianniprocida/ </li>
     <li>Navigate to the habit-tracker directory: cd habit-tracker</li>
     <li>Run the python script to create the database with pricing data of BTC,ETH, EOS, LTC
        : python3.8 Load2mysql 
        </li>
     <li>Run the script 'createClosingPrice.sql' to create a new table named "closingprice" in the database, and establish relationships between the "closingprice" table
         and any existing tables in the database as necessary.</li>
   </ul>     
<h2>Features</h2>
<h3>Creating habits</h3>

```
tracker = HabitTracker("John")
tracker.addHabit("Brush your teeth","2023-03-01","2023-03-4","D")
tracker.addHabit("Go to school","2023-03-02","2023-04-30","D")
```

<h3>Deleting habits</h3>
To delete a habit, use the delete method:

```
tracker.deleteHabit("Go to school")
```

<h3>Searching by name</h3>
To search for a habit, use the search_by_name method:

```
(myhabit,index) = tracker.search_by_name("Brush your teeth")
```

<h3>Searching by id</h3>

```
output = tracker.search_by_id(1)
```

<h3>Checking off by name</h3>

```
tracker.checkoff_by_name("Brush your teeth","y")
tracker.checkoff_by_name("Brush your teeth","y")
```
    <ul>
        <li>analysis.py -> data visualization </li>
        <li>Load2mysql.py -> populate a mysql database with pricing data from each csv file</li>
        <li>scraper.py -> downloads pricing data from <a href="https://www.cryptodatadownload.com/data/binance/">Click here</a> </li>
        <li>createClosingPrice.sql -> define relationships between tables.Insert data into the closingPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
        <li>createOpeningPrice.sql -> define relationships between tables. Insert data into the OpeningPrice (referencing table) from other tables i.e. BTCUSDT,ETHUSDT,EOSUSDT,LTCUSDT (referenced tables)</li>
    </ul>

</body>


