
use Cryptocurrencies;

create table OpeningPrice (id int not null,Date datetime not null,primary key(id)); 


insert into OpeningPrice (id,Date) select id,date from BTCUSDT;


alter table OpeningPrice 
add constraint fk_btc_op
foreign key(Date) references BTCUSDT(date);

alter table OpeningPrice add column BTC decimal(12,4);

update OpeningPrice o inner join BTCUSDT b on o.Date = b.Date set o.BTC=b.open;



alter table OpeningPrice 
add constraint fk_eth_op
foreign key(Date) references ETHUSDT(date);

alter table OpeningPrice add column ETH decimal(12,4);

update OpeningPrice o inner join ETHUSDT e on o.Date = e.Date set o.ETH=e.open;




alter table OpeningPrice 
add constraint fk_eos_op
foreign key(Date) references EOSUSDT(date);

alter table OpeningPrice add column EOS decimal(12,4);

update OpeningPrice o inner join EOSUSDT e on o.Date = e.Date set o.EOS = e.open;


alter table OpeningPrice 
add constraint fk_ltc_op
foreign key(Date) references LTCUSDT(date);

alter table OpeningPrice add column LTC decimal(12,4);

update OpeningPrice o inner join LTCUSDT l on o.Date = l.Date set o.EOS = l.open;


