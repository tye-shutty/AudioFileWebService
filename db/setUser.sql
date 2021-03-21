DELIMITER //
DROP PROCEDURE IF EXISTS setUser //
CREATE PROCEDURE setUser
(
   /* Parameters */
   IN email_in VARCHAR(200),
   IN new_email_in VARCHAR(200),
   IN admin_status_in BOOLEAN
)
BEGIN
   /* Do the INSERT */
  UPDATE users 
  SET admin_status = admin_status_in,
      email = new_email_in 
  WHERE email = email_in;

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'Unable to update the user.';
   END IF;

END //
DELIMITER ;
