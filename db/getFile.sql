/* This SQL requests a specfic folder */
DELIMITER //
DROP PROCEDURE IF EXISTS getFile //
CREATE PROCEDURE getFile
(
   /* Parameters */
   IN id_in int
)
BEGIN
  SELECT * FROM files WHERE file_id = id_in;

END //
DELIMITER ;
