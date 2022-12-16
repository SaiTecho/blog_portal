create database blog_portal;
use blog_portal;

create table user(userid int primary key auto_increment, username varchar(255), email varchar(255) unique, password varchar(255));





create table post(
postId int NOT NULL auto_increment primary key,
Title VARCHAR(250) NOT NULL,
body  text null default null,
published DATETIME NOT NULL,
updated DATETIME DEFAULT NULL,
userId int NOT NULL,
categoryname varchar(255) not null,
foreign key (userId) references user(userid)

);



show tables;
select * from post;
-- Drop table post;

-- insert into post(Title, body,published, updated, userId, categoryname) values("Title", "body","2022-09-19 12:22:22", "2022-09-19 12:22:22", 1, "IT");
-- insert into post(Title, body,published, updated, userId, categoryname) values("Title", "body","2022-09-19 12:22:22", "2022-09-19 12:22:22", 1, "IT");
-- insert into post(Title, body,published, updated, userId, categoryname) values("Title", "body","2022-09-19 12:22:22", "2022-09-19 12:22:22", 1, "IT");
-- insert into post(Title, body,published, updated	, userId, categoryname) values("Title", "body","2022-09-20 12:22:22", "2022-09-20 12:22:22", 1, "IT");