CREATE SCHEMA school;

CREATE TABLE school.teachers (
    teacher_id INT PRIMARY KEY,
    first_tname VARCHAR(255), 
	last_tname VARCHAR(255)
);

CREATE TABLE school.subjects (
    subject_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE school.groups(
    group_id INT PRIMARY KEY,
	group_name VARCHAR(255) NOT NULL

);

CREATE TABLE school.students(
   student_id INT PRIMARY KEY ,
   first_sname VARCHAR (255) NOT NULL,
   last_sname VARCHAR(255) NOT NULL,
   group_id INT NOT NULL,
 
   FOREIGN KEY (group_id) REFERENCES school.groups (group_id) ON DELETE CASCADE ON UPDATE CASCADE
 
);

CREATE TABLE school.subject_teacher (
	subject_id INT NOT NULL,
	teacher_id INT NOT NULL,
	group_id INT NOT NULL,
	FOREIGN KEY (subject_id) REFERENCES school.subjects (subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (teacher_id) REFERENCES school.teachers (teacher_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (group_id) REFERENCES school.groups (group_id) ON DELETE CASCADE ON UPDATE CASCADE
);
 
CREATE TABLE school.marks(
    mark_id INT PRIMARY KEY,
	student_id INT NOT NULL,
	subject_id INT NOT NULL,
	date_ DATE,
	mark INT,
	FOREIGN KEY (subject_id) REFERENCES school.subjects (subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (student_id) REFERENCES school.students (student_id) ON DELETE CASCADE ON UPDATE CASCADE
);