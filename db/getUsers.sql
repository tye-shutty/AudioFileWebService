DELIMITER //
DROP PROCEDURE IF EXISTS getUsers //
CREATE PROCEDURE getUsers
(
   /* Parameters */
)
BEGIN
  select email from users where admin_status = 0;

END //
DELIMITER ;
