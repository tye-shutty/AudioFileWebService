DROP TABLE IF EXISTS folders;
CREATE TABLE folders (
  folder_id INT NOT NULL AUTO_INCREMENT,
  folder_name VARCHAR(600) NOT NULL,
  folder_description VARCHAR(60000),
  parent INT DEFAULT 0, /** 0 means no parent*/
  owner_email VARCHAR(200),
  PRIMARY KEY (folder_id)
);
