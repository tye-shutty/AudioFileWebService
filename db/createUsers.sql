DROP TABLE IF EXISTS users;
CREATE TABLE users (
  email VARCHAR(200) NOT NULL,
  admin_status BOOLEAN NOT NULL,
  PRIMARY KEY (email)
);
