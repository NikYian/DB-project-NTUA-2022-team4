DROP schema IF EXISTS hfri_db;
create schema hfri_db;
use hfri_db;




create table hfri_executive (
executive_id int unsigned not null auto_increment,
first_name varchar(20) not null,
last_name varchar(20) not null,
date_of_birth date not null check(year(date_of_birth) < 2000),
hfri_governing_body varchar(20) not null check(hfri_governing_body in ('General Assembly','Scientific Council','Advisory Commitee','Deputy Directors')), 
primary key (executive_id)
);

create table hfri_programs (
program_id int unsigned not null auto_increment,
program_name varchar(50) not null,
hfri_governing_body varchar(30) not null check(hfri_governing_body in ('General Assembly','Scientific Council','Advisory Commitee','Deputy Directors')), 
primary key (program_id)
);

create table organization_ (
organization_id int unsigned not null auto_increment,
abbreviation varchar(10),
organization_name varchar(100),
street_name varchar(30) not null,
street_number int unsigned,
postal_code varchar(10) not null,
city varchar(50),

primary key (organization_id)
);

create table university (
organization_id int unsigned,
ministry_budget double(7,2) not null,
PRIMARY KEY (organization_id),
CONSTRAINT FK_university
	FOREIGN KEY (organization_id) REFERENCES organization_ (organization_id) on delete cascade on update cascade
);



create table research_center (
organization_id int unsigned,
ministry_budget double(7,2) not null,
private_funding double(7,2) not null,
PRIMARY KEY (organization_id),
CONSTRAINT FK_RS
	FOREIGN KEY (organization_id) REFERENCES organization_ (organization_id) on delete cascade on update cascade
);

create table company (
organization_id int unsigned,
equity double(7,2) not null,
PRIMARY KEY (organization_id),
CONSTRAINT FK_company
	FOREIGN KEY (organization_id) REFERENCES organization_ (organization_id) on delete cascade on update cascade
);

create table phone_number(
organization_id int unsigned, 
phone_number varchar(30),
PRIMARY KEY (organization_id,phone_number),
CONSTRAINT FK_phone
	FOREIGN KEY (organization_id) REFERENCES organization_ (organization_id) on delete restrict on update cascade
);

create table researcher (
researcher_id int unsigned not null auto_increment,
first_name varchar(20) not null,
last_name varchar(20) not null,
gender varchar(10) check(gender in ('male','female','other')),
date_of_birth date not null check(year(date_of_birth) < 2000),
organization_id int unsigned not null,
start_date date not null,

primary key (researcher_id),
constraint researcher_age_check check (year(start_date) - year(date_of_birth) > 21),
constraint researcher_start_date_check check (start_date < '2022-06-05'),
CONSTRAINT FK_researcher
	FOREIGN KEY (organization_id) REFERENCES organization_ (organization_id) on delete restrict on update cascade

);



create table project (
project_id int unsigned not null auto_increment,
title varchar(50) not null,
summary text(100) not null,
funding double(2,2) not null,  /* constraint check funding in millions */
start_date date not null,
end_date date,
duration int unsigned,
evaluator int unsigned,
rating double(3,2) unsigned not null,
accountable int unsigned, 
program_id int unsigned,
executive_id int unsigned,
organization_id int unsigned,

primary key (project_id),
CONSTRAINT FK_evaluator FOREIGN KEY (evaluator) REFERENCES researcher(researcher_id) on delete restrict on update cascade,
CONSTRAINT FK_accountable FOREIGN KEY (accountable) REFERENCES researcher(researcher_id) on delete restrict on update cascade,
CONSTRAINT FK_program FOREIGN KEY (program_id) REFERENCES hfri_programs(program_id) on delete restrict on update cascade,
CONSTRAINT FK_exec FOREIGN KEY (executive_id) REFERENCES hfri_executive(executive_id) on delete restrict on update cascade,
CONSTRAINT FK_organization FOREIGN KEY (organization_id) REFERENCES organization_(organization_id) on delete restrict on update cascade,


-- CONSTRAINT project_ck_1 check(duration = datediff(start_date,end_date)),
constraint project_ck_2 check (1*365<= duration and duration <= 4*365),
constraint project_ck_3 check (start_date < '2022-06-05'),
constraint project_ck_4 check(funding >= 0.1 and funding <= 1.00),
-- constraint project_ck_5 check(rating>4.9),
constraint project_ck_6 check(evaluator<>accountable)
/* accountable can't be also evaluator */

);



create table works_on (

researcher_id int unsigned,
project_id int unsigned,

PRIMARY KEY (researcher_id, project_id),
CONSTRAINT FK_works_on_project
	FOREIGN KEY (project_id) REFERENCES project (project_id) on delete restrict on update cascade,
CONSTRAINT FK_works_on_researcher
	FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id) on delete restrict on update cascade
);



create table field_of_research(
field_of_research varchar(100) not null,

primary key (field_of_research)
);

create table project_field (
project_id int unsigned,
field_of_research varchar(100) not null,

PRIMARY KEY (project_id,field_of_research),
CONSTRAINT FK_FR_project
	FOREIGN KEY (project_id) REFERENCES project (project_id) on delete restrict on update cascade,
CONSTRAINT FK_FR_FR
	FOREIGN KEY (field_of_research) REFERENCES field_of_research (field_of_research) on delete restrict on update cascade
);

create table deliverable (
deliverable_id int unsigned not null auto_increment,
project_id int unsigned,
title varchar(100) not null,
summary varchar(100) not null,
due_date date not null,
-- πρεπει να είναι μικρότερη από την ημερομηνία λήξης του project

primary key (deliverable_id),
CONSTRAINT FK_deliverable
	FOREIGN KEY (project_id) REFERENCES project (project_id) on delete restrict on update cascade
);


/* VIEWS */

create view projects_per_researcher as
select r.researcher_id, r.first_name, r.last_name, p.project_id , p.title
from  researcher r
inner join works_on wo on wo.researcher_id = r.researcher_id 
inner join project p on wo.project_id = p.project_id 
order by r.researcher_id;


create view projects_per_program as
select hp.program_id, hp.program_name, p.project_id , p.title
from  hfri_programs hp  
inner join project p on hp.program_id  = p.program_id 
order by hp.program_id;






















