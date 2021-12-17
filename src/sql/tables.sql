create table shops
(
	id serial primary key,
	name character varying(100) unique not null,
	add_date date not null
);


create table prices
(
	price_date date not null,
	price real not null,
	product_id integer references products (id) on delete cascade  not null,
	shop_id integer 
);