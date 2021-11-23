CREATE TABLE lol_item_table (
	lol_item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
   	lol_item_name CHAR NOT NULL,
	lol_item_explain CHAR NOT NULL,
	lol_item_buy_price INTEGER,
	lol_item_sell_price INTEGER,
	lol_item_tag CHAR NOT NULL,
	lol_item_reference_pics CHAR,
	table_constraints);
