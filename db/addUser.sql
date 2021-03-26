/* This SQL file adds a user to the Database */
DELIMITER //
DROP PROCEDURE IF EXISTS addUser //
CREATE PROCEDURE addUser
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN admin_status_in BOOLEAN
)
BEGIN
   SET @y = (SELECT count(*) FROM users WHERE email=email_in);
   IF (@y = 0) THEN
      
      INSERT INTO users (email, admin_status) 
      VALUES (email_in, admin_status_in);

      /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
      IF(ROW_COUNT() = 0) THEN
         SIGNAL SQLSTATE '52711'
         SET MESSAGE_TEXT = 'Unable to create the user.';
      END IF;
   ELSE 
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to create the user.';
   END IF;

END //
DELIMITER ;
