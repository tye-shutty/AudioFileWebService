DELIMITER //
DROP PROCEDURE IF EXISTS findFileString //
CREATE PROCEDURE findFileString
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN search_string VARCHAR(600)
)
BEGIN
   select file_id from files INNER JOIN folders on (files.parent = folders.folder_id) 
   WHERE owner_email = email_in AND (file_description like search_string or file_name like search_string);

END //
DELIMITER ;
