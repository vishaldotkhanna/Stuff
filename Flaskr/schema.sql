drop table if exists posts;

create table posts(pid integer primary key autoincrement,
title text not null,
content text not null,
date text);

drop table if exists users;

create table users(uid integer primary key autoincrement,
username text unique not null,
password text not null,
email text not null);


