# Take-Home-Coding-Assessment

Building a backened API for a small library that lends books to members,The API will be written in FastApi,backend by a relational database and accessed through HTTP endpoints documented automatically via FastApi OpenAPI integration.


First step: https://www.youtube.com/watch?v=0sOvCWFmrtA (Watched this video in youtube)


Teknologjitë e Përdorura (Tech Stack):
Python (FastAPI)
PostgreSQL (Databaza)
SQLAlchemy / Alembic (ORM dhe Migrimet)
Psycopg (Lidhja me DB)


Struktura e databazes:
Members te cilat permbajne keto kolona : id(primary key),full_name,email(unique),join_date si dhe is_active.Relationships (1:M Loans)
Authors te cilat permbajne keto kolona:authors_id(primary key),full_name si dhe country.Relationships (M:N Books)
Categories te cilat permbajne keto kolona:categories_id(primary key) si dhe name(unique).Relationships (1:M with books)
Books te cilat permbajne keto kolona:book_id(primary key),title,isbn(unique),category_id(foreign key),total_copies(>=0),published_year.Relationships (M:1 ctagories,M:N authors si dhe 1:M loans)
Book_authors te cilat permbajne keto kolona:book_id,author_id(composite PK).Relationships (M:N books and authors)
Loans te cilat permbajne keto kolona:loans_id(primary key),member_id(foreign key),book_id(foreign key),loan_date,due_date,return_date(Null=active loan).Relationships(M:1 Members si dhe M:1 Books)


Instalimi dhe konfigurimi:
1.pip install fastapi[all]
2.instalimi i Postgre SQL
3.pip install "psycopg[binary]"
4.pip install alembic
5.uvicorn app.main:app --reload (kjo e nis serverin)


Routers endpoints:
http://localhost:8000/docs
1.Members.py CRUD(GET,POST,PUT,DELETE)
2.Authors.py CRUD(GET,POST,PUT,DELETE)
3.Categories.py CRUD(GET,POST,PUT,DELETE)  
4.Books.py CRUD(GET,POST,PUT,DELETE)
5.Loans.py CRUD(GET,POST,PUT,DELETE)
6.Books_py.py CRUD(GET,POST,PUT,DELETE)

Repository structure:
ReadMe.md ==>> Ne pika tshkurta projekti
Reasoning ==> Ne pika te gjata projekti
requirements.txt ==> Teknologjitë e Përdorura
main.py ==> API routers
models.py ==>> tabelat SQLAlchemy
schemas.py ==> Pydantic schmas(BaseModel)
database.py ==>> lidhja me Postgre SQL
alembic ==>> historiku i databazes
tests ==>>pytest

