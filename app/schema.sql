create table if not exists PATIENT(PatId varchar(20) primary key, Fname varchar(20),Lname varchar(20), Email varchar(30), Password varchar(30), Phone BigInt(10));
create table if not EXISTS DOCTOR(DocId varchar(20) primary key, Fname varchar(20),Lname varchar(20), Speciality varchar(25),Email varchar(30), Password varchar(30),Phone BigInt(10));
create table if not EXISTS DEPARTMENT(DeptId int(3) primary key, Dname varchar(30), Head varchar(20) references DOCTOR(DocId) on delete set NULL);

