/* This SQL requests a list of Users with no admin status */
DELIMITER //
DROP PROCEDURE IF EXISTS getUsers //
CREATE PROCEDURE getUsers
(
   /* Parameters */
)
BEGIN
  SELECT email FROM users WHERE admin_status = 0;

END //
DELIMITER ;
