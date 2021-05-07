DROP TABLE IF EXISTS users;
CREATE TABLE users (
  email VARCHAR(200) NOT NULL,
  admin_status BOOLEAN NOT NULL,
  pswd VARCHAR(200),
  PRIMARY KEY (email)
);
