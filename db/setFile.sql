DELIMITER //
DROP PROCEDURE IF EXISTS setFile //
CREATE PROCEDURE setFile
(
   /* Parameters */
   IN id_in INT,
   IN new_name VARCHAR(200),
   IN new_description VARCHAR(200),
   IN plays_in INT,
   IN last_played_in TIMESTAMP,
   IN parent_in INT
)
BEGIN
   /**Folder parent and owner is fixed*/
   UPDATE files
   SET file_name = new_name,
      file_description = new_description,
      last_played = last_played_in,
      times_played = plays_in,
      parent = parent_in

   WHERE file_id = id_in;

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to update the file.';
   END IF;

END //
DELIMITER ;
