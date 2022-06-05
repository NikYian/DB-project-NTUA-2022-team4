import faker
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

fake = faker.Faker()
content = "";



#Organization

DUMMY_DATA_NUMBER = 145;
TABLE_NAME = "organization_";
TABLE_COLUMNS = ["abbreviation", "organization_name", "street_number", "street_name", "postal_code", "city"]


content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"NTUA"}", "{"National Technical University of Athens"}", "{"42"}", "{"Patission str"}", "{"10682"}", "{"Athens"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"AUEB"}", "{"Athens University of Economics and Business"}", "{"4"}", "{" Karaoli"}", "{"80112"}", "{"Athens"}" );\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"DUTH"}", "{"Democritus University of Thrace"}", "{"10"}", "{"Thoukididou "}", "{"17455"}", "{"Thrace"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"A.U.Th"}", "{"Aristotle University of Thessaloniki"}", "{"11"}", "{"Chiou"}", "{"10438"}", "{"Thessaloniki"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"UoC"}", "{"University of Crete"}", "{"12"}", "{"Iraklio"}", "{"70013"}", "{"Iraklio"}");\n'

for _ in range(DUMMY_DATA_NUMBER):
    abbreviation = ""
    organization_name = fake.company()
    for a in organization_name: 
        if (a.isupper()) == True: 
            abbreviation += a 
    street_number = np.random.randint(1,200)
    street_name = fake.street_name()
    postal_code = fake.postcode()
    city = fake.city()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{abbreviation}", "{organization_name}","{street_number}","{street_name}","{postal_code}", "{city}");\n'



#university

DUMMY_DATA_NUMBER = 50;
TABLE_NAME = "university";
TABLE_COLUMNS = ["organization_id", "ministry_budget"]

for i in range(DUMMY_DATA_NUMBER):
    organization_id = i+1
    ministry_budget = np.round(np.random.rand(1)[0],2)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{organization_id}", "{ministry_budget}");\n'
x = organization_id
#research_center

DUMMY_DATA_NUMBER = 50;
TABLE_NAME = "research_center";
TABLE_COLUMNS = ["organization_id", "ministry_budget", "private_funding"]

for i in range(DUMMY_DATA_NUMBER):
    organization_id = i+x
    ministry_budget = np.round(np.random.rand(1)[0],2)
    private_funding = np.round(np.random.rand(1)[0],2)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{organization_id}", "{ministry_budget}", "{private_funding}");\n'
x = organization_id


#company

DUMMY_DATA_NUMBER = 50;
TABLE_NAME = "company";
TABLE_COLUMNS = ["organization_id", "equity"]

for i in range(DUMMY_DATA_NUMBER):
    organization_id = i+x
    equity = np.round(np.random.rand(1)[0],2)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{organization_id}", "{equity}");\n'


# researcher 

DUMMY_DATA_NUMBER = 3000;
TABLE_NAME = "researcher";
TABLE_COLUMNS = ["first_name", "last_name", "date_of_birth", "gender","organization_id", "start_date"]


for _ in range(DUMMY_DATA_NUMBER):
    gender = np.random.choice(["male", "female", "other"])
    first_name = fake.first_name_male() if (gender=="male") else fake.first_name_female()
    last_name = fake.last_name()
    date_of_birth = fake.date_between_dates(date_start=datetime(1955,1,1), date_end=datetime(1992,12,31))
    x = date_of_birth + relativedelta(years= 22)
    organization_id = np.random.randint(1,150)
    start_date = fake.date_between_dates(date_start= x, date_end=datetime(2015,12,31))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{first_name}", "{last_name}", "{date_of_birth}",  "{gender}","{organization_id}",   "{start_date}");\n'

#hfri_executive
DUMMY_DATA_NUMBER = 100;
TABLE_NAME = "hfri_executive";
TABLE_COLUMNS = ["first_name", "last_name", "date_of_birth", "hfri_governing_body"]

for i in range(DUMMY_DATA_NUMBER):
    coin = np.random.randint(1,3);
    first_name = fake.first_name_male() if (coin==1) else fake.first_name_female()
    last_name = fake.last_name()
    date_of_birth = fake.date_between_dates(date_start=datetime(1955,1,1), date_end=datetime(1992,12,31))
    hfri_governing_body = np.random.choice(["General Assembly", "Scientific Council","Deputy Directors","Advisory Commitee"])
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{first_name}", "{last_name}", "{date_of_birth}",  "{hfri_governing_body}");\n'



#hfri_programs
DUMMY_DATA_NUMBER = 70;
TABLE_NAME = "hfri_programs";
TABLE_COLUMNS = ["program_name", "hfri_governing_body"]

for i in range(DUMMY_DATA_NUMBER):
    program_name = "Program " + str(i+1)
    hfri_governing_body = np.random.choice(["General Assembly", "Scientific Council","Deputy Directors","Advisory Commitee"])
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{program_name}", "{hfri_governing_body}");\n'



#active projects and deliverables

DUMMY_DATA_NUMBER = 700;
TABLE_NAME = "project";
TABLE_NAME2 = "deliverable";
TABLE_COLUMNS = ["title", "summary", "funding", "start_date", "end_date", "duration", "evaluator", "accountable", "program_id", "executive_id", "organization_id"]
TABLE_COLUMNS2 = ["project_id", "title","summary", "due_date"]

for i in range(DUMMY_DATA_NUMBER):
    funding = np.round(np.random.rand(1)[0],2) 
    while (funding < 0.1  or funding >= 1.00):
        funding = np.round(np.random.rand(1)[0],2) 
    title = "Project "+str(i+1)
    summary = fake.text(100)
    start_date = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2022,5,31))
    x = start_date + relativedelta(years= 1)
    y = start_date + relativedelta(years= 4)
    end_date = fake.date_between_dates(date_start=x, date_end=y)
    duration = int(str(end_date - start_date).split(" ")[0])
    evaluator = np.random.randint(1,30)
    accountable = np.random.randint(1,50)
    if (evaluator == accountable): accountable += 1
    program_id = np.random.randint(1,30);
    executive_id = np.random.randint(1,100);
    organization_id = np.random.randint(1,150);
    if i>=20 and i<33:
        organization_id = 1
        start_date = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2018,12,31))
    x = start_date + relativedelta(years= 1)
    y = start_date + relativedelta(years= 4)
    if i>=60 and i<73:
        organization_id = 1
        start_date = fake.date_between_dates(date_start=datetime(2019,1,1), date_end=datetime(2019,12,31))
    x = start_date + relativedelta(years= 1)
    y = start_date + relativedelta(years= 4)
    end_date = fake.date_between_dates(date_start=x, date_end=y)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{title}", "{summary}", "{funding}", "{start_date}",  "{end_date}", "{duration}",   "{evaluator}", "{accountable}", "{program_id}", "{executive_id}", "{organization_id}");\n'
    del_num = np.random.randint(0,4);
    for j in range(del_num):
        project_id = i+1
        title = "Deliverable "+str(j+1)
        summary = fake.text(100)
        due_date = fake.date_between_dates (start_date,end_date)
        content += f'INSERT INTO {TABLE_NAME2} ({",".join(TABLE_COLUMNS2)}) VALUES ("{project_id}", "{title}",  "{summary}", "{due_date}");\n'

#finsished projects
t= project_id

DUMMY_DATA_NUMBER = 300;
TABLE_NAME = "project";
TABLE_COLUMNS = ["title", "summary", "funding", "start_date", "end_date", "duration", "evaluator", "accountable", "program_id", "executive_id", "organization_id"]

for i in range(DUMMY_DATA_NUMBER):
    funding = np.round(np.random.rand(1)[0],2) 
    while (funding < 0.1  or funding >= 1.00):
        funding = np.round(np.random.rand(1)[0],2)    
    if (funding <= 0.1  or funding == 1.00): funding = 0.42
    title = "Project "+str(i+t)
    summary = fake.text(100)
    start_date = fake.date_between_dates(date_start=datetime(2010,1,1), date_end=datetime(2015,12,31))
    x = start_date + relativedelta(years= 1)
    y = start_date + relativedelta(years= 4)
    end_date = fake.date_between_dates(date_start=x, date_end=y)
    duration = int(str(end_date - start_date).split(" ")[0])
    #appoved = np.random.choice(["Y","N"])
    evaluator = np.random.randint(1,30);
    accountable = np.random.randint(1,50);
    program_id = np.random.randint(1,30);
    executive_id = np.random.randint(1,100);
    organization_id = np.random.randint(1,150);
    if (evaluator == accountable): accountable += 1;
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{title}", "{summary}", "{funding}", "{start_date}",  "{end_date}", "{duration}",   "{evaluator}", "{accountable}", "{program_id}", "{executive_id}", "{organization_id}");\n'
    del_num = np.random.randint(0,4);
    for j in range(del_num):
        project_id = i+t
        title = "Deliverable "+str(j+1)
        summary = fake.text(100)
        due_date = fake.date_between_dates (start_date,end_date)
        content += f'INSERT INTO {TABLE_NAME2} ({",".join(TABLE_COLUMNS2)}) VALUES ("{project_id}", "{title}",  "{summary}", "{due_date}");\n'
   




#works_on

DUMMY_DATA_NUMBER = 5000;
TABLE_NAME = "works_on";
TABLE_COLUMNS = ["researcher_id", "project_id"]

for i in range(3000):
    researcher_id = i+1;
    project_num = np.random.randint(1,10);
    arr = np.random.choice(1000, project_num, replace=False)
    project_id1 = ((i) % 1000)+1
    if project_id1 == 1001: project_id1 = 1000
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{researcher_id}", "{project_id1}");\n'
    for j in range(project_num):
        project_id = arr[j] + 1;
        if (project_id != project_id1):
            content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{researcher_id}", "{project_id}");\n'


#phone_number

TABLE_NAME = "phone_number";
TABLE_COLUMNS = ["organization_id", "phone_number"]

for i in range(150):
    organization_id = i +1
    n = np.random.randint(1,4);
    for _ in range(n):
        phone_number = fake.phone_number()
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{organization_id}", "{phone_number}");\n'


#field_of_research

TABLE_NAME = "field_of_research";
TABLE_COLUMNS = ["field_of_research"]

content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Economics"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Biology"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Chemistry"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Physics"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Space sciences"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Astronomy"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Computer science"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Mathematics"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Systems science"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Agriculture"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Architecture and design"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Education"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Engineering and technology"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Environmental studies and forestry"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Medicine"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Anthropology"}");\n'
content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{"Linguistics and languages"}");\n'




# project_field

TABLE_NAME = "project_field";
TABLE_COLUMNS = ["project_id", "field_of_research"]

for i in range(1000):
    project_id = i+1
    n = np.random.randint(1,4);
    arr = np.random.choice(["Linguistics and languages", "Anthropology","Medicine","Environmental studies and forestry","Engineering and technology","Education",
        "Architecture and design", "Agriculture","Systems science", "Mathematics","Computer science", "Astronomy", "Space sciences",
        "Physics", "Chemistry","Biology","Economics" ],n,False)
    for j in range(n):
        field_of_research = arr[j]
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{project_id}", "{field_of_research}");\n'


with open(f"dummy_data.sql", 'w') as f:
    f.write(content) 


