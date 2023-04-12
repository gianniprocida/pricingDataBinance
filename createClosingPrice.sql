
use pricingdata;

/* 
Adds an artificial column to BTC,ETH,EOS, and LTC tables. This step is necessay because of the slicing of the datasets
(see the Load2mysql.py script). myidx will help me with fast query e.g. select * from BTC where myidx = 1 (instead of
select * from BTC where date = "2021-01-02" )
*/

ALTER TABLE BTC ADD COLUMN myidx INT DEFAULT 0;

set @btc = 0;

UPDATE BTC SET myidx = (@btc := @btc + 1) LIMIT 1020;



ALTER TABLE ETH ADD COLUMN myidx INT DEFAULT 0;

set @eth = 0;

UPDATE ETH SET myidx = (@eth := @eth + 1) LIMIT 1020;




/*-- Adding foreign key constraint to link BTC table with closingprice table. Not sure whether that's the proper way to do it
but for the sake of the simplicity, I'll keep it like that.
*/
create table if not exists closingprice (id int not null,Date datetime not null,primary key(Date)); 

alter table closingprice
add constraint fk_btc_cl
foreign key(Date) references BTC(date);

insert into closingprice (id,Date) select myidx,date from BTC;

alter table closingprice add column BTC decimal(12,4);

/*updating closingprice table using join
*/
update closingprice c inner join BTC b on c.Date = b.date set c.BTC=b.close;


/*-- Adding foreign key constraint to link ETH table with closingprice table. 
*/
alter table closingprice 
add constraint fk_eth_cl
foreign key(Date) references ETH(date);

alter table closingprice add column ETH decimal(12,4);

update closingprice c inner join ETH e on c.Date = e.date set c.ETH=e.close;



/*-- Adding foreign key constraint to link EOS table with closingprice table. 
*/
alter table closingprice 
add constraint fk_eos_cl
foreign key(Date) references EOS(date);

alter table closingprice add column EOS decimal(12,4);

/*updating closingprice table using join
*/
update closingprice c inner join EOS e on c.Date = e.date set c.EOS = e.close;


/*-- Adding foreign key constraint to link EOS table with closingprice table. 
*/
alter table closingprice 
add constraint fk_ltc_cl
foreign key(Date) references LTC(date);

alter table closingprice add column LTC decimal(12,4);

update closingprice c inner join LTC l on c.Date = l.date set c.LTC = l.close;


