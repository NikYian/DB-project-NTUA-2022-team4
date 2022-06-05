create index program_index on hfri_programs(program_name);
create index title_index on project(title);
create index end_date_index on project(end_date);
create index r_full_name_index on researcher(first_name, last_name);
create index field_of_research_index1 on project_field(field_of_research);
create index organization_name_index on organization_(organization_name);
create index start_date_index on project(start_date);
create unique index field_of_research_index2 on field_of_research(field_of_research);
create index projectID_index1 on project_field(project_id);
create unique index researcherID_index on researcher(researcher_id);
create index date_of_birth_index on researcher(date_of_birth);
create index funding_index on project(funding);
create unique index projectID_index2 on project(project_id);
create index e_full_name_index on hfri_executive(first_name, last_name);


delimiter //
CREATE TRIGGER check_evaluator_insert BEFORE INSERT on works_on
FOR EACH ROW
BEGIN
  IF new.researcher_id in (select evaluator from project where project_id = new.project_id) THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Cant put this researcher_id on works_on table';
  END IF;
END;//

delimiter ;

delimiter //
CREATE TRIGGER check_evaluator_update BEFORE UPDATE on works_on
FOR EACH ROW
BEGIN
  IF new.researcher_id in (select evaluator from project where project_id = new.project_id) THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Cant put this researcher_id on works_on table';
  END IF;
END;//

delimiter ;

