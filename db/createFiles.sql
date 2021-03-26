DROP TABLE IF EXISTS files;
CREATE TABLE files (
  file_id INT NOT NULL AUTO_INCREMENT,
  file_name VARCHAR(200) NOT NULL,
  file_description VARCHAR(600),
  parent INT NOT NULL DEFAULT 0, /** 0 means no parent*/
  upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  last_played TIMESTAMP,
  times_played INT DEFAULT 0,
  PRIMARY KEY (file_id)
);
