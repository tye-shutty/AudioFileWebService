/* This SQL file deletes a requested folder */
DELIMITER //
DROP PROCEDURE IF EXISTS deleteFile //
CREATE PROCEDURE deleteFile
(
   /* Parameters */
   IN id_in VARCHAR(200)
)
BEGIN
   DELETE FROM files WHERE file_id = id_in;
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Unable to delete the file.';
   END IF;

END //
DELIMITER ;
