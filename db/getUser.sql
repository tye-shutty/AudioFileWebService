DELIMITER //
DROP PROCEDURE IF EXISTS getUser //
CREATE PROCEDURE getUser
(
   /* Parameters */
   IN email_in VARCHAR(200)
)
BEGIN
  select * from users where email = email_in;

END //
DELIMITER ;
