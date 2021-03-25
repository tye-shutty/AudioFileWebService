/* This SQL file adds a folder into the database */
DELIMITER //
DROP PROCEDURE IF EXISTS addFolder //
CREATE PROCEDURE addFolder
(
   /* Parameters */
   IN folder_name_in VARCHAR(200),
   IN folder_description_in VARCHAR(600),
   IN parent_in INT
)
BEGIN

   declare x int default 0;  
   SELECT COUNT(*) INTO x FROM folders WHERE folder_id=parent_in; 
   
   /* Do the INSERT */
   IF (x != 0) THEN
      INSERT INTO folders (folder_name, folder_description, parent)
      VALUES (folder_name_in, folder_description_in, parent_in);
      /* If the INSERT is successful, then this will return the Id for the record */
      SELECT LAST_INSERT_ID();
   ELSE
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to create the folder.';
   END IF;

END //
DELIMITER ;
