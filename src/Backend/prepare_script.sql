CREATE DATABASE IF NOT EXISTS spm_g2t7;
USE spm_g2t7;

CREATE TABLE staff (
	staff_id INT PRIMARY KEY NOT NULL,
    staff_fname VARCHAR(50) NOT NULL,
    staff_lname VARCHAR(50) NOT NULL,
    dept VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    access_rights INT NOT NULL,
    FOREIGN KEY (access_rights) REFERENCES access_rights(access_id)
);

CREATE TABLE access_rights (
	access_id INT PRIMARY KEY NOT NULL,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE role (
	role_id INT AUTO_INCREMENT NOT NULL,
	role_name VARCHAR(20) NOT NULL,
    role_desc LONGTEXT NOT NULL,
    PRIMARY KEY (role_id, role_name)
);

CREATE TABLE skill (
	skill_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	skill_name VARCHAR(50) NOT NULL,
    skill_desc LONGTEXT NOT NULL
);

CREATE TABLE role_skill (
    skill_name VARCHAR(50) NOT NULL ,
	role_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (skill_name, role_name),
    FOREIGN KEY (role_name) REFERENCES role(role_name)
);

CREATE TABLE staff_skill (
	staff_id INT NOT NULL,
    skill_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (staff_id, skill_name),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (skill_name) REFERENCES skill(skill_name)
);

CREATE TABLE role_applicant (
	role_name VARCHAR(20),
    staff_id INT,
    comments LONGTEXT NULL,
    creation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (role_name, staff_id),
    FOREIGN KEY (role_name) REFERENCES role(role_name),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

INSERT INTO access_rights VALUES 
(1, 'Admin'),
(2, 'Staff'),
(3, 'Human Resource'),
(4, 'Manager'),
(5, 'Director');

INSERT INTO staff VALUES 
(00123451, 'Kevin', 'Oleary','Director','kevino@aio.com', '5'),
(00123452, 'Mark', 'Cuban','Director','markc@aio.com', '5'),
(00123456, 'Johnny', 'Tan','Sales','jonnyt@aio.com', '2'),
(00123457, 'Sarah', 'Lim','IT','saraht@aio.com', '2'),
(00123458, 'Bob', 'Toh','Finance','bobt@aio.com', '2'),
(00123459, 'Shermaine', 'Tee','Human Resource','shermainet@aio.com', '3'),
(00123460, 'Gallywix', 'Howdy','Admin','gallywixh@aio.com', '1');

INSERT INTO role VALUES
(00001, 'Account Manager', 'Handle customer account under the Sales Division'),
(00002, 'Support Team', 'Provide IT support under the System Solutioning Division'),
(00003, 'Junior Engineer', 'Junior Software Engineer under the Engineering Division'),
(00004, 'Senior Engineer', 'Senior Software Engineer under the Engineering Division'),
(00005, 'Finance Executive', 'Assist with payroll-related matters under the Finance Division');

INSERT INTO skill VALUES 
(00001, 'Microsoft Excel', 'Comfortable with creating and debugging simple Macro'),
(00002, 'Microsoft Powerpoint', 'Comfortable with creating powerpoint slides'),
(00003, 'Python', 'Familiar with python syntax and able to code a simple program'),
(00004, 'Calculus', 'Able to comfortably solve for partial derivatives'),
(00005, 'Java', 'Familiar with Java syntax and able to code a simple program');

INSERT INTO staff_skill VALUES
(00123456, 00001),
(00123456, 00005),
(00123457, 00001),
(00123458, 00003),
(00123458, 00004),
(00123452, 00001),
(00123452, 00004),
(00123459, 00002);

INSERT INTO role_skill VALUES 
(00003, 00001),
(00003, 00003),
(00004, 00001),
(00004, 00003),
(00004, 00005),
(00005, 00001),
(00005, 00002),
(00005, 00004);

INSERT INTO role_applicant (role_name, staff_id, comments) VALUES 
(00003, 00123457, 'I have always had a deep passion in software engineering. During my free time I have taken up multiple software-related certifications.'),
(00004, 00123452, 'While I may not have the necessary skillset at the moment, I am very passionate to learn.'),
(00005, 00123458, 'Finance is my passion'),
(00002, 00123456, 'Interested in the Sales Division');