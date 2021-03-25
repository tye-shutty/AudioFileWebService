/* This SQL file deletes a user from the database */
DELIMITER //
DROP PROCEDURE IF EXISTS deleteUser //
CREATE PROCEDURE deleteUser
(
   /* Parameters */
   IN email_in VARCHAR(200)
)
BEGIN
  DELETE FROM users WHERE email = email_in;

   /*ROW_COUNT() returns the number of rows updated, inserted or deleted by the preceding statement.*/
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Unable to delete the user.';
   END IF;

END //
DELIMITER ;
