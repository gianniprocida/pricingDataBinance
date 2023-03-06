
use Cryptocurrencies;

create table ClosingPrice (id int not null,Date datetime not null,BTC decimal(12,4),primary key(id)); 

alter table ClosingPrice 
add constraint fk_btc
foreign key(Date) references BTCUSDT(date);

insert into ClosingPrice (id,Date,BTC) select id,date,close from BTCUSDT;


alter table ClosingPrice 
add constraint fk_eth
foreign key(Date) references ETHUSDT(date);

alter table ClosingPrice add column ETH decimal(12,4);

update ClosingPrice c inner join ETHUSDT e on c.Date = e.Date set c.ETH=e.close;




alter table ClosingPrice 
add constraint fk_eos
foreign key(Date) references EOSUSDT(date);

alter table ClosingPrice add column EOS decimal(12,4);

update ClosingPrice c inner join EOSUSDT e on c.Date = e.Date set c.EOS = e.close;


alter table ClosingPrice 
add constraint fk_ltc
foreign key(Date) references LTCUSDT(date);

alter table ClosingPrice add column LTC decimal(12,4);

update ClosingPrice c inner join LTCUSDT l on c.Date = l.Date set c.EOS = l.close;


