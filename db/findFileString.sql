DELIMITER //
DROP PROCEDURE IF EXISTS findFileString //
CREATE PROCEDURE findFileString
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN search_string VARCHAR(600)
)
BEGIN
   SELECT file_id FROM files INNER JOIN folders ON (files.parent = folders.folder_id) 
   WHERE owner_email = email_in AND (file_description LIKE search_string OR file_name LIKE search_string);

END //
DELIMITER ;
