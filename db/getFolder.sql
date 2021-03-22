DELIMITER //
DROP PROCEDURE IF EXISTS getFolder //
CREATE PROCEDURE getFolder
(
   /* Parameters */
   IN id_in int
)
BEGIN
  select * from folders where folder_id = id_in;

END //
DELIMITER ;
