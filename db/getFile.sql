/* This SQL requests a specfic folder */
DELIMITER //
DROP PROCEDURE IF EXISTS getFile //
CREATE PROCEDURE getFile
(
   /* Parameters */
   IN id_in int
)
BEGIN
  SELECT file_id, file_name, file_description, files.parent, upload_date, last_played, times_played, owner_email
  FROM files 
  INNER JOIN folders on (files.parent = folders.folder_id)
  WHERE file_id = id_in;

END //
DELIMITER ;
