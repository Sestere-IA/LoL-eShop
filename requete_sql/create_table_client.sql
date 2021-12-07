CREATE TABLE client_table (
	client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
   	client_identifiant CHAR NOT NULL,
	client_password CHAR NOT NULL,
	client_money INTEGER DEFAULT 0,
	client_is_admin BIT DEFAULT 0);
