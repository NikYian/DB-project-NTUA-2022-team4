from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_mysqldb import MySQL
from pandas import concat
from hfri_db import app, db ## initially created by __init__.py, need to be used here
from hfri_db.forms import StudentForm
import json

@app.route("/")
def index():
    try:
        cur = db.connection.cursor()

        cur.execute("select * from field_of_research")
        column_names = [i[0] for i in cur.description]
        field = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        
        #q34
        morethan=[{'name':'1'},{'name':'2'},{'name':'3'},{'name':'4'},{'name':'5'}, {'name':'6'}, {'name':'7'}, {'name':'8'}, {'name':'9'}, {'name':'10'}]

        return render_template("landing.html",
                               pageTitle = "Landing Page",
                               field=field, morethan = morethan)
    except Exception as e:
        print(e)
        return render_template("landing.html", pageTitle = "Landing Page")


@app.route("/Q31")
def Q31():
    try:
        cur = db.connection.cursor()
        query = "select * from hfri_programs;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        

        return render_template("Q31.html",table = table,   pageTitle = "Q31")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q31res3", methods =  ["GET", "POST"] )
def Q31res3():
    try:
        cur = db.connection.cursor()
        query = "select executive_id,concat(last_name,' ',first_name) as name,hfri_governing_body from hfri_executive;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        

        return render_template("Q31res3.html",table = table,   pageTitle = "Q31")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q31res", methods = ["GET", "POST"])
def Q31res():
    try:        
        date = request.form.get('date')
        duration = request.form.get('duration')
        exec = request.form.get('exec')
        if date and (not duration) and (not exec):
            after = str(request.form.get("after"))
            before = str(request.form.get("before"))
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id =  p.executive_id where start_date < '"+before+"' and start_date >'"+after+ "' order by start_date"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif duration and (not date) and (not exec):
            dur = request.form.get("dur")
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id =  p.executive_id where duration < " +dur + " order by duration"         
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif exec and (not date) and (not duration):
            exec = request.form.get("field_select")
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id where e.executive_id = " + exec        
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif exec and date and (not duration):
            exec = request.form.get("field_select")
            after = str(request.form.get("after"))
            before = str(request.form.get("before"))
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id where e.executive_id = " + exec +" and start_date < '"+before+"' and start_date >'"+after+ "' order by start_date"       
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif exec and date and duration:
            dur = request.form.get("dur")
            exec = request.form.get("field_select")
            after = str(request.form.get("after"))
            before = str(request.form.get("before"))
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id where e.executive_id = " + exec +" and p.duration < " +dur +" and start_date < '"+before+"' and start_date >'"+after+ "' order by project_id"       
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif exec and duration and (not date):
            dur = request.form.get("dur")
            exec = request.form.get("field_select")
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id where e.executive_id = " + exec +" and p.duration < " +dur +" order by project_id"       
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        elif (not exec) and date and duration:
            dur = request.form.get("dur")
            after = str(request.form.get("after"))
            before = str(request.form.get("before"))
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id where  p.duration < " +dur +" and start_date < '"+before+"' and start_date >'"+after+ "' order by project_id"       
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        else:
            query = "select p.project_id,p.title, p.summary, p.funding,p.start_date,p.end_date,p.duration, concat(e.last_name,' ',e.first_name) as hfri_executive from project p inner join hfri_executive e on e.executive_id = p.executive_id order by p.project_id  "       
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
        return render_template("Q31res.html",table = table, pageTitle = "Q31 Projects")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/Q31res2", methods = ["GET", "POST"])
def Q31res2():
    try:
        select = str(request.form.get("btn"))
        cur = db.connection.cursor()
        query = "select r.first_name, r.last_name, r.researcher_id from researcher r inner join works_on w on w.researcher_id = r.researcher_id inner join project p on p.project_id = w.project_id where p.project_id = " + select
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q31res2.html", table = table, select = select, pageTitle = "Q31 Researchers")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q321")
def Q321():
    try:
        cur = db.connection.cursor()
        query = "select * from projects_per_researcher order by project_id, researcher_id"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q321.html", table = table, pageTitle = "Q321")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q322")
def Q322():
    try:
        cur = db.connection.cursor()
        query = "select * from projects_per_program order by program_id, project_id"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q322.html", table = table, pageTitle = "Q322")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/Q33", methods = ["GET", "POST"])
def Q33():
    try:
        select = str(request.form.get("field_select"))
        #Projects in Field
        cur = db.connection.cursor()
        query = "select pr.title,pf.field_of_research,pr.end_date from project pr inner join project_field pf on pr.project_id = pf.project_id where pf.field_of_research ='"+select+"' and pr.end_date > curdate() order by pr.end_date "

        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()

        #Researchers in Field
        cur = db.connection.cursor()
        query = "select r.first_name,r.last_name,year(p.end_date) as end_year, p.title as project_name, pf.field_of_research from researcher r inner join works_on w on r.researcher_id = w.researcher_id inner join project p on p.project_id = w.project_id inner join project_field pf on p.project_id = pf.project_id where pf.field_of_research ='"+select+"' and (p.end_date > curdate() or year(p.end_date) = year(curdate()))"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q33.html", projects = projects, researchers = researchers, select = select, pageTitle = "Q33")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/Q34", methods = ["GET", "POST"])
def Q34():
    try:
        mt = str(request.form.get("morethan"))
        cur = db.connection.cursor()
        query = "select t.organization_name, t.start_year as year_A ,t.projects_in_year as projects_in_year_A, t1.start_year as year_B, t1.projects_in_year as projects_in_year_B from (select o.organization_name as organization_name , year(pr.start_date) as start_year, count(*) as projects_in_year,  (year(pr.start_date) + 1) as next_year from organization_ o inner join project pr on o.organization_id = pr.organization_id group by start_year, o.organization_name order by projects_in_year desc) t inner join (select o.organization_name as organization_name , year(pr.start_date) as start_year, count(*) as projects_in_year,  (year(pr.start_date) + 1) as next_year from organization_ o inner join project pr on o.organization_id = pr.organization_id group by start_year, o.organization_name order by projects_in_year desc) t1 on t.next_year = t1.start_year and t.organization_name = t1.organization_name having projects_in_year_A = projects_in_year_B and projects_in_year_A >" +mt+ " order by t.organization_name,t.start_year;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        orgs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q34.html", orgs = orgs, mt = mt, pageTitle = "Q34")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/Q35")
def Q35():
    try:
        cur = db.connection.cursor()
        cur.execute("set @row_num = 0; DROP table IF EXISTS temp; CREATE TEMPORARY TABLE temp select @row_num := @row_num + 1 as id, fr1.field_of_research as fr1, fr2.field_of_research as fr2 from field_of_research fr1 CROSS JOIN field_of_research fr2 where fr1.field_of_research > fr2.field_of_research and fr1.field_of_research <> fr2.field_of_research; DROP table IF EXISTS temp2; CREATE TEMPORARY TABLE temp2 select t.id, pf1.project_id, t.fr1, t.fr2 from temp t inner join project_field pf1 on pf1.field_of_research = t.fr1 inner join project_field pf2 on pf2.field_of_research = t.fr2 where pf1.project_id = pf2.project_id group by pf1.project_id,t.id order by t.id; ")

        query = "select t.fr1, t.fr2, count(t.id) as count from temp2 t group by t.fr1, t.fr2 order by count desc limit 3;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        fc = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q35.html", fc = fc, pageTitle = "Q35")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q36")
def Q36():
    try:
        cur = db.connection.cursor()
        cur.execute("DROP table IF EXISTS temp36; CREATE TEMPORARY TABLE temp36 select r.researcher_id, first_name, last_name, timestampdiff(year, date_of_birth, curdate()) as age, count(*) as num_projects from researcher r inner join works_on w on r.researcher_id=w.researcher_id inner join project p on w.project_id=p.project_id where curdate()<p.end_date group by researcher_id having age<40 order by num_projects desc;")
        query = "select * from (select r.researcher_id, first_name, last_name, timestampdiff(year, date_of_birth, curdate()) as age, count(*) as num_projects from researcher r inner join works_on w on r.researcher_id=w.researcher_id inner join project p on w.project_id=p.project_id where curdate()<p.end_date group by researcher_id having age<40 order by num_projects desc) t where t.num_projects = (select num_projects from temp36 limit 1);"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q36.html", res = res, pageTitle = "Q36")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q37")
def Q37():
    try:
        cur = db.connection.cursor()
        query = "select first_name, last_name,e.executive_id, o.organization_name, sum(p.funding) as tot_funding from hfri_executive e inner join project p on e.executive_id=p.executive_id inner join organization_ o on p.organization_id=o.organization_id inner join company c on c.organization_id = o.organization_id group by e.executive_id, o.organization_id order by tot_funding desc limit 5;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        exec = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q37.html", exec =exec, pageTitle = "Q37")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/Q38")
def Q38():
    try:
        cur = db.connection.cursor()
        query = "select r.first_name,r.last_name,count(p1.project_id) as num_projects from researcher r inner join works_on w on r.researcher_id = w.researcher_id inner join (select project_id from project p1 where project_id not in (select p2.project_id from project p2 inner join deliverable d on d.project_id = p2.project_id)) as p1 on p1.project_id = w.project_id group by r.first_name,r.last_name having (count(p1.project_id) >= 5) order by num_projects desc;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("Q38.html", r =r, pageTitle = "Q38")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/alltables")
def alltables():
    try:
        cur = db.connection.cursor()
        cur.execute("show tables")
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("alltables.html", r =r, pageTitle = "HFRI DB Tables")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)



@app.route("/view", methods = ["GET", "POST"])
def tableView():
    try:
        args = request.args
        table_name = args.get('table')
        delete = args.get('delete')
        add = args.get('add')

        cur = db.connection.cursor()
        query = "SELECT * FROM " + table_name
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()


        if add=='1':
            query = "INSERT INTO " + table_name +" ("
            query += ",".join(column_names)
            query += ") VALUES (" 
            values = []
            for col in column_names:
                value = request.form.get(col)
                value = "'" + value +"'"
                values.append(value)
            query += ",".join(values)
            query += ")" 
            cur = db.connection.cursor()
            cur.execute(query)
            cur.close() 


        if delete=='1':
            colid =  str(args.get('colid'))
            delval = str(args.get('delval'))
            cur = db.connection.cursor()
            query = "DELETE FROM " + table_name + " WHERE " + colid +" = '" + delval +"'"
            cur.execute(query)
            cur.close() 

        cur = db.connection.cursor()
        query = "SELECT * FROM " + table_name
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        #r = {str(key): str(value) for key, value in r}
        cur.close()

        return render_template("view_table.html", results = r, column_names=column_names, table_name = table_name, pageTitle = table_name)

        #return jsonify({"results": r, "column_names": column_names})
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        return render_template("view_table.html", results = r, column_names=column_names, table_name = table_name, pageTitle = table_name)


@app.route("/edit", methods = ["GET", "POST"])
def edit():
    try:
        args = request.args
        table_name = args.get('table')
        update = args.get('update')
        colid =  str(args.get('colid'))
        edval = str(args.get('edval'))
                     
        cur = db.connection.cursor()
        query = "SELECT * FROM " + table_name + " WHERE " + colid +" = '" + edval +"'"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()

        if update=='1':
            query = "UPDATE " + table_name +" SET "
            values = []
            for col in column_names:
                    value = request.form.get(col)
                    if value != r[0][col]:
                        value = col + "= '" + value +"'"
                        values.append(value)
            query += ",".join(values)
            query += " WHERE " + colid +" = '" + edval +"';"
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()   
            cur.close() 

                     
        cur = db.connection.cursor()
        query = "SELECT * FROM " + table_name + " WHERE " + colid +" = '" + edval +"'"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()

        return render_template("edit_table.html", results = r, column_names=column_names, table_name = table_name, pageTitle = table_name)

        #return jsonify({"results": r, "column_names": column_names})
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        cur = db.connection.cursor()
        query = "SELECT * FROM " + table_name + " WHERE " + colid +" = '" + edval +"'"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        r = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("edit_table.html", results = r, column_names=column_names, table_name = table_name, pageTitle = "Update " + table_name)

