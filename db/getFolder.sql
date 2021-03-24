/* This SQL requests a specfic folder */
DELIMITER //
DROP PROCEDURE IF EXISTS getFolder //
CREATE PROCEDURE getFolder
(
   /* Parameters */
   IN id_in int
)
BEGIN
  SELECT * FROM folders WHERE folder_id = id_in;

END //
DELIMITER ;
