CREATE TABLE item_table (
	item_id INTEGER PRIMARY KEY AUTOINCREMENT,
   	item_name CHAR NOT NULL,
	item_explain CHAR NOT NULL,
	item_buy_price INTEGER,
	item_sell_price INTEGER,
	item_tag CHAR NOT NULL,
	item_img_path CHAR,
	table_constraints);
