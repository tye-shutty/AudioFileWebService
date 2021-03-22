DELIMITER //
DROP PROCEDURE IF EXISTS deleteFolder //
CREATE PROCEDURE deleteFolder
(
   /* Parameters */
   IN id_in VARCHAR(200)
)
BEGIN
  delete from folders where folder_id = id_in;

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Unable to delete the folder.';
   END IF;

END //
DELIMITER ;
