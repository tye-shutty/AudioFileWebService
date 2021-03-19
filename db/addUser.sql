DELIMITER //
DROP PROCEDURE IF EXISTS addUser //
CREATE PROCEDURE addUser
(
   /* Parameters */
   IN email VARCHAR(200),
   IN admin_status BOOLEAN
)
BEGIN
   /* Do the INSERT */
  INSERT INTO users (email, admin_status) VALUES
  (email, admin_status);

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to create the user.';
   END IF;

END //
DELIMITER ;
