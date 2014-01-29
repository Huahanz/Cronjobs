CREATE DATABASE stock

CREATE TABLE IF NOT EXISTS stocks
(
id int(11) NOT NULL,
symbol varchar(255) NOT NULL,
pattern varchar(255) NOT NULL,
min int(11) DEFAULT 0,
max int(11) DEFAULT 10000,
PRIMARY KEY (id)
);
