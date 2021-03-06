DELIMITER //
DROP PROCEDURE IF EXISTS findFolderString //
CREATE PROCEDURE findFolderString
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN search_string VARCHAR(600)
)
BEGIN
   select folder_id from folders where owner_email = email_in and (folder_description like search_string or folder_name like search_string); 
END //
DELIMITER ;
