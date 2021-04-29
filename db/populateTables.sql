
INSERT INTO users (admin_status, email) VALUES
(0,'person@domain.com'),
(0,'p2@domain.com'),
(0,'p3@domain.com');

INSERT INTO folders (folder_name, owner_email) VALUES
('root','person@domain.com'),
('root','p2@domain.com'),
('home','p3@domain.com');

INSERT INTO files (file_name, file_description, parent, last_played, times_played) VALUES
('song1','',1,NULL,0),
('secret','done',2, NULL,0),
('work','',3, CURRENT_TIMESTAMP(),1);
