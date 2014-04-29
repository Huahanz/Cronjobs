CREATE DATABASE mt;

/**
The state based mt data store.
 */
CREATE TABLE IF NOT EXISTS mt_state_based
(
url varchar(255) NOT NULL,
state BIGINT NOT NULL,
state_extension varchar(255) NOT NULL,
start_pattern varchar(255) NOT NULL,
end_pattern varchar(255) NOT NULL,
extract_start_pattern varchar(255) NOT NULL,
extract_info varchar(255) NOT NULL,
PRIMARY KEY (url)
);


INSERT INTO mt_state_based values
('www.test.com', 123, 'aaa', '%saa', '%sseee', 'abc', '123');