-- 3.1

select program_name from hfri_programs order by length(program_name),program_name;
select start_date from project order by start_date;
select duration from project order by duration;
select concat(last_name,' ',first_name) as hfri_executive from hfri_executive order by last_name;

select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive
from project p
inner join hfri_executive e on e.executive_id =  p.executive_id
where e.executive_id = 10 
;

select r.first_name, r.last_name, r.researcher_id
from researcher r
inner join works_on w on w.researcher_id = r.researcher_id
inner join project p on p.project_id = w.project_id
where p.project_id = 4;


-- 3.3 
select pr.title,pf.field_of_research,pr.end_date from project pr 
inner join project_field pf on pr.project_id = pf.project_id
where pf.field_of_research = 'Biology' and pr.end_date > curdate();

select r.first_name,r.last_name,year(p.end_date) as end_year, p.title as project_name, pf.field_of_research from researcher r 
inner join works_on w on r.researcher_id = w.researcher_id
inner join project p on p.project_id = w.project_id
inner join project_field pf on p.project_id = pf.project_id
where pf.field_of_research = 'Biology' and (p.end_date > curdate() or year(p.end_date) = year(curdate())-1) ;

-- 3.4
/*
DROP table IF EXISTS temp_3_4;
CREATE TEMPORARY TABLE temp_3_4
select o.organization_name as organization_name , year(pr.start_date) as start_year, count(*) as projects_in_year,  (year(pr.start_date) + 1) as next_year 
from organization_ o
inner join project pr on o.organization_id = pr.organization_id
group by start_year, o.organization_name
order by projects_in_year desc;

select t.organization_name, t.start_year as year_A ,t.projects_in_year as projects_in_year_A, t1.start_year as year_B, t1.projects_in_year as projects_in_year_B
from temp_3_4 t
inner join temp_3_4 t1 
on t.next_year = t1.start_year and t.organization_name = t1.organization_name
having projects_in_year_A = projects_in_year_B and projects_in_year_A > 4
order by t.organization_name,t.start_year; */

select t.organization_name, t.start_year as year_A ,t.projects_in_year as projects_in_year_A, t1.start_year as year_B, t1.projects_in_year as projects_in_year_B
from (select o.organization_name as organization_name , year(pr.start_date) as start_year, count(*) as projects_in_year,  (year(pr.start_date) + 1) as next_year 
from organization_ o
inner join project pr on o.organization_id = pr.organization_id
group by start_year, o.organization_name
order by projects_in_year desc) t
inner join (select o.organization_name as organization_name , year(pr.start_date) as start_year, count(*) as projects_in_year,  (year(pr.start_date) + 1) as next_year 
from organization_ o
inner join project pr on o.organization_id = pr.organization_id
group by start_year, o.organization_name
order by projects_in_year desc) t1
on t.next_year = t1.start_year and t.organization_name = t1.organization_name
having projects_in_year_A = projects_in_year_B and projects_in_year_A > 4
order by t.organization_name,t.start_year;

/*
-- test 3.4
select * from temp_3_4
order by organization_name, start_year;
*/

-- 3.5

set @row_num = 0;
select  t.fr1, t.fr2, count(t.id) as count
from (select t.id, pf1.project_id, t.fr1, t.fr2
from (select @row_num := @row_num + 1 as id, fr1.field_of_research as fr1, fr2.field_of_research as fr2
from field_of_research fr1
CROSS JOIN  field_of_research fr2
where fr1.field_of_research > fr2.field_of_research and fr1.field_of_research <> fr2.field_of_research) t
inner join project_field pf1
on pf1.field_of_research = t.fr1
inner join  project_field pf2
on pf2.field_of_research = t.fr2
where pf1.project_id = pf2.project_id
group by pf1.project_id,t.id 
order by t.id) t
group by  t.fr1, t.fr2
order by count desc limit 3;

-- 3.6

DROP table IF EXISTS temp36;
CREATE TEMPORARY TABLE temp36
select r.researcher_id, first_name, last_name, timestampdiff(year, date_of_birth, curdate()) as age, count(*) as num_projects
from researcher r 
inner join works_on w on r.researcher_id=w.researcher_id 
inner join project p on w.project_id=p.project_id 
where curdate()<p.end_date 
group by researcher_id
having age<40 
order by num_projects desc;

select * from (select r.researcher_id, first_name, last_name, timestampdiff(year, date_of_birth, curdate()) as age, count(*) as num_projects
from researcher r 
inner join works_on w on r.researcher_id=w.researcher_id 
inner join project p on w.project_id=p.project_id 
where curdate()<p.end_date 
group by researcher_id
having age<40 
order by num_projects desc) t
where t.num_projects = (select num_projects from temp36 limit 1);

-- 3.7
select first_name, last_name, o.organization_name, max(p.funding) as top_funding 
from hfri_executive e 
inner join project p on e.executive_id=p.executive_id 
inner join organization_ o on p.organization_id=o.organization_id 
inner join company c on c.organization_id = o.organization_id
group by e.executive_id 
order by o.organization_id desc
limit 5;

-- 3.8
select r.first_name,r.last_name,count(p1.project_id) as num_projects
from researcher r
inner join works_on w on r.researcher_id = w.researcher_id
inner join 
(select project_id from project p1
where project_id not in
		(select p2.project_id
		from project p2 
		inner join deliverable d on d.project_id = p2.project_id)) as p1
on p1.project_id = w.project_id
group by r.first_name,r.last_name
having (count(p1.project_id) >= 5);









