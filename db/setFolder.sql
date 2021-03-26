DELIMITER //
DROP PROCEDURE IF EXISTS setFolder //
CREATE PROCEDURE setFolder
(
   /* Parameters */
   IN id_in INT,
   IN new_name VARCHAR(200),
   IN new_description VARCHAR(200)
)
BEGIN
   /**Folder parent and owner is fixed*/
   UPDATE folders
   SET folder_name = new_name,
      folder_description = new_description
   WHERE folder_id = id_in;

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to update the folder.';
   END IF;

END //
DELIMITER ;
