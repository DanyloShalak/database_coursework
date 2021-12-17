create or replace function get_product_id(product_name text)
returns integer as $$
	declare return_id integer;
			record_count integer;
	begin 
		select count(*) from products where products.name = get_product_id.product_name into record_count;
		if record_count = 0 then
			insert into products(name, add_date) values(get_product_id.product_name, current_date);
		end if;
		select id from products where products.name = get_product_id.product_name into return_id;
		return return_id;
	end;
$$ language plpgsql;


create or replace function get_shop_id(shop_name text)
returns integer as $$
	declare return_id integer;
			record_count integer;
	begin 
		select count(*) from shops where shops.name = get_shop_id.shop_name into record_count;
		if record_count = 0 then
			insert into shops(name, add_date) values(get_shop_id.shop_name, current_date);
		end if;
		select id from shops where shops.name = get_shop_id.shop_name into return_id;
		return return_id;
	end;
$$ language plpgsql;



CREATE or replace FUNCTION check_unique() RETURNS trigger AS $emp_stamp$
	declare record_count integer;
    BEGIN
        select count(*) from prices where prices.product_id = new.product_id 
				and prices.price_date = new.price_date into record_count;
		if record_count = 0 then
			return new;
		elsif record_count = 1 then
			update prices 
			set price = new.price, shop_id = new.shop_id
			where product_id = new.product_id and price_date = new.price_date;
			return null;
		end if;
    END;
$emp_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER unique_price_records BEFORE INSERT ON prices
    FOR EACH ROW EXECUTE PROCEDURE check_unique();
