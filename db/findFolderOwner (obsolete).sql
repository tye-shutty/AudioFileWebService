DELIMITER //
DROP PROCEDURE IF EXISTS findFolderOwner //
DROP PROCEDURE IF EXISTS `debug_msg` //

CREATE PROCEDURE debug_msg(enabled INTEGER, msg VARCHAR(255))
BEGIN
  IF enabled THEN
    select concat('** ', msg) AS '** DEBUG:';
  END IF;
END //

CREATE PROCEDURE findFolderOwner
(
   /* Parameters */
   IN folder_id_in INT
)
BEGIN
   declare x int default 0; /*all declares must be at start double dash (--) comments don't work*/
   declare z int default 1; 
   declare w int default 0; 
   declare e VARCHAR(200) default "wrong user"; 
   declare y VARCHAR(200) default "not root";
   select count(*) into x from folders where folder_id=folder_id_in; 
   IF (x = 0) THEN
      SIGNAL SQLSTATE '52711'
      SET MESSAGE_TEXT = 'No folder.';
   END IF;
   
   SET x = folder_id_in;

   -- SET @enabled = TRUE;
   -- call debug_msg(@enabled, 'my first debug message');
   -- call debug_msg(@enabled, (select concat_ws('','arg1:', y)));
   -- call debug_msg(TRUE, 'This message always shows up');
   -- call debug_msg(FALSE, 'This message will never show up');

   WHILE (z=1) DO  
      select folder_name into y from folders where folder_id=x;
      IF (y = "root") THEN
         SET z = 0;
         SELECT email into e from users where root_folder = x;
      ELSE 
         select parent into w from folders where folder_id=x; 
         SET x = w;
      END IF;
   END WHILE;
   SELECT e;

END //
DELIMITER ;
