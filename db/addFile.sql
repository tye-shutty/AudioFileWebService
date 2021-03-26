/* This SQL file adds a folder into the database */
DELIMITER //
DROP PROCEDURE IF EXISTS addFile //
CREATE PROCEDURE addFile
(
   /* Parameters */
   IN file_name_in VARCHAR(200),
   IN file_description_in VARCHAR(600),
   IN parent_in INT,
   IN owner_email_in VARCHAR(200)
)
BEGIN

   declare x int default 0;  
   SELECT COUNT(*) INTO x FROM folders WHERE folder_id=parent_in AND owner_email = owner_email_in; 
   
   /* Do the INSERT if parent exists*/
   IF (x != 0) THEN
      INSERT INTO files (file_name, file_description, parent)
      VALUES (file_name_in, file_description_in, parent_in);
      /* If the INSERT is successful, then this will return the Id for the record */
      SELECT LAST_INSERT_ID();
   ELSE
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to create the file.';
   END IF;

END //
DELIMITER ;
