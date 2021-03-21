DELIMITER //
DROP PROCEDURE IF EXISTS addUser //
CREATE PROCEDURE addUser
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN admin_status_in BOOLEAN
)
BEGIN
   SET @y = (SELECT count(*) from users where email=email_in);
   IF (@y = 0) THEN
      /* Do the INSERT */
      INSERT INTO folders (folder_name)
      VALUES ("root");
      /* If the INSERT is successful, then this will return the Id for the record */
      SET @x = LAST_INSERT_ID();
      
      INSERT INTO users (email, admin_status, root_folder) 
      VALUES (email_in, admin_status_in, @x);

      /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
      IF(ROW_COUNT() = 0) THEN
         DELETE FROM folders WHERE folder_id = @x;
         SIGNAL SQLSTATE '52711'
         SET MESSAGE_TEXT = 'Unable to create the user.';
      END IF;
   ELSE 
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to create the user.';
   END IF;

END //
DELIMITER ;
