
use Cryptocurrencies;

create table if not exists ClosingPrice (id int not null,Date datetime not null,primary key(id)); 

alter table ClosingPrice
add constraint fk_btc_cl
foreign key(Date) references BTCUSDT(date);

insert into ClosingPrice (id,Date) select id,date from BTCUSDT;

alter table ClosingPrice add column BTC decimal(12,4);

update ClosingPrice c inner join BTCUSDT b on c.Date = b.date set c.BTC=b.close;



alter table ClosingPrice 
add constraint fk_eth_cl
foreign key(Date) references ETHUSDT(date);

alter table ClosingPrice add column ETH decimal(12,4);

update ClosingPrice c inner join ETHUSDT e on c.Date = e.date set c.ETH=e.close;




alter table ClosingPrice 
add constraint fk_eos_cl
foreign key(Date) references EOSUSDT(date);

alter table ClosingPrice add column EOS decimal(12,4);

update ClosingPrice c inner join EOSUSDT e on c.Date = e.date set c.EOS = e.close;


alter table ClosingPrice 
add constraint fk_ltc_cl
foreign key(Date) references LTCUSDT(date);

alter table ClosingPrice add column LTC decimal(12,4);

update ClosingPrice c inner join LTCUSDT l on c.Date = l.date set c.LTC = l.close;


