DROP DATABASE IF EXISTS spm_g2t7;
CREATE DATABASE spm_g2t7;
USE spm_g2t7;

CREATE TABLE access_rights (
	access_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE staff (
	staff_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    current_role VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    access_rights INT NOT NULL,
    FOREIGN KEY (access_rights) REFERENCES access_rights(access_id)
);

CREATE TABLE role (
	role_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	role_name VARCHAR(20) NOT NULL,
    role_description LONGTEXT NOT NULL,
    listed_by INT NOT NULL,
    no_of_pax INT NOT NULL,
    department varchar(50) not null,
    location varchar(50) not null,
    expiry_timestamp INT NOT NULL 
);

CREATE TABLE skill (
	skill_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	skill_name VARCHAR(50) NOT NULL,
    skill_description LONGTEXT NOT NULL
);

CREATE TABLE role_skill (
    role_id INT NOT NULL,
	skill_id INT NOT NULL,
    PRIMARY KEY (role_id, skill_id),
    FOREIGN KEY (role_id) REFERENCES role(role_id),
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id)
);

CREATE TABLE staff_skill (
	staff_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (staff_id, skill_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id)
);

CREATE TABLE role_applicant (
	role_id INT NOT NULL,
    staff_id INT NOT NULL,
    comments LONGTEXT NULL,
    creation_timestamp INT NOT NULL,
    PRIMARY KEY (role_id, staff_id),
    FOREIGN KEY (role_id) REFERENCES role(role_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

INSERT INTO access_rights VALUES 
(1, 'Staff'),
(2, 'Administrator');

INSERT INTO staff VALUES 
(00123451, 'Kevin', 'Oleary','Director', 'Personal Assistant', 'kevino@aio.com', 1),
(00123452, 'Mark', 'Cuban','Director','Secretary', 'markc@aio.com', 1),
(00123456, 'Johnny', 'Tan','Sales', 'Sales Associate', 'jonnyt@aio.com', 1),
(00123457, 'Sarah', 'Lim','IT', 'IT Associate', 'saraht@aio.com', 1),
(00123458, 'Bob', 'Toh','Finance', 'Finance Manager', 'bobt@aio.com', 1),
(001234588, 'Bob', 'Toh','Finance', 'Finance Manager', 'bobt@aio.com', 2),
(00123459, 'Shermaine', 'Tee','Human Resource', 'Talent Acquisition', 'shermainet@aio.com', 1),
(001234599, 'Shermaine', 'Tee','Human Resource', 'Talent Acquisition', 'shermainet@aio.com', 2),
(00123460, 'Gallywix', 'Howdy','IT', 'Administrator', 'gallywixh@aio.com', 1),
(001234600, 'Gallywix', 'Howdy','IT', 'Administrator', 'gallywixh@aio.com', 2);

INSERT INTO role VALUES
(00001, 'Account Manager', 'Handle customer account under the Sales Division', '00123459', 3, 'Sales', 'Singapore', 1701388800),
(00002, 'Support Team', 'Provide IT support under the System Solutioning Division', '00123459', 1, 'IT', 'Singapore', 1701388800),
(00003, 'Junior Engineer', 'Junior Software Engineer under the Engineering Division', '00123459', 2, 'IT', 'India', 1701388800),
(00004, 'Senior Engineer', 'Senior Software Engineer under the Engineering Division', '00123459', 2, 'IT', 'India', 1701388800),
(00005, 'Finance Executive', 'Assist with payroll-related matters under the Finance Division', '00123459', 1, 'Sales', 'Malaysia', 1701388800);

INSERT INTO skill VALUES 
(00001, 'Microsoft Excel', 'Comfortable with creating and debugging simple Macro'),
(00002, 'Microsoft Powerpoint', 'Comfortable with creating powerpoint slides'),
(00003, 'Python', 'Familiar with python syntax and able to code a simple program'),
(00004, 'Calculus', 'Able to comfortably solve for partial derivatives'),
(00005, 'Java', 'Familiar with Java syntax and able to code a simple program');

INSERT INTO staff_skill VALUES
(00123451, 00002),
(00123451, 00004),
(00123452, 00001),
(00123452, 00004),
(00123456, 00001),
(00123456, 00005),
(00123457, 00001),
(00123458, 00003),
(00123458, 00004),
(00123459, 00004),
(00123460, 00002),
(00123460, 00003);


INSERT INTO role_skill VALUES 
(00001, 00004),
(00002, 00002),
(00002, 00003),
(00003, 00001),
(00003, 00003),
(00004, 00001),
(00004, 00003),
(00004, 00005),
(00005, 00001),
(00005, 00002),
(00005, 00004);

INSERT INTO role_applicant VALUES 
(00003, 00123457, 'I have always had a deep passion in software engineering. During my free time I have taken up multiple software-related certifications.', 1695174041),
(00004, 00123452, 'While I may not have the necessary skillset at the moment, I am very passionate to learn.', 1695174041),
(00005, 00123458, 'Finance is my passion', 1695174041),
(00002, 00123456, 'Interested in the Sales Division', 1695174041);