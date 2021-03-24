/* This SQL requests for specific user */
DELIMITER //
DROP PROCEDURE IF EXISTS getUser //
CREATE PROCEDURE getUser
(
   /* Parameters */
   IN email_in VARCHAR(200)
)
BEGIN
  SELECT * FROM users WHERE email = email_in;

END //
DELIMITER ;
