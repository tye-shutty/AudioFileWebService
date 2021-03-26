/* This SQL file deletes a requested folder */
DELIMITER //
DROP PROCEDURE IF EXISTS deleteFolder //
CREATE PROCEDURE deleteFolder
(
   /* Parameters */
   IN id_in VARCHAR(200)
)
BEGIN
   /* Check if has children before deleting */
   declare x int default 0; 
   SELECT COUNT(*) INTO x FROM folders WHERE parent=id_in; 
   IF (x = 0) THEN
      DELETE FROM folders WHERE folder_id = id_in;
   ELSE
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Unable to delete the folder.';
   END IF;

END //
DELIMITER ;
