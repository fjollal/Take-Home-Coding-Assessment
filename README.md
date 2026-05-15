# Take-Home-Coding-Assessment

Building a backened API for a small library that lends books to members,The API will be written in FastApi,backend by a relational database and accessed through HTTP endpoints documented automatically via FastApi OpenAPI integration.


First step: https://www.youtube.com/watch?v=0sOvCWFmrtA (Watched this video in youtube)


Teknologjitë e Përdorura (Tech Stack):
<br>
Python (FastAPI)
<br>
PostgreSQL (Databaza)
<br>
SQLAlchemy / Alembic (ORM dhe Migrimet)
<br>
Psycopg (Lidhja me DB)


Struktura e databazes:
<br>
Members te cilat permbajne keto kolona : id(primary key),full_name,email(unique),join_date si dhe is_active.Relationships (1:M Loans)
<br>
Authors te cilat permbajne keto kolona:authors_id(primary key),full_name si dhe country.Relationships (M:N Books)
<br>
Categories te cilat permbajne keto kolona:categories_id(primary key) si dhe name(unique).Relationships (1:M with books)
<br>
Books te cilat permbajne keto kolona:book_id(primary key),title,isbn(unique),category_id(foreign key),total_copies(>=0),published_year.Relationships (M:1 ctagories,M:N authors si dhe 1:M loans)
<br>
Book_authors te cilat permbajne keto kolona:book_id,author_id(composite PK).Relationships (M:N books and authors)
<br>
Loans te cilat permbajne keto kolona:loans_id(primary key),member_id(foreign key),book_id(foreign key),loan_date,due_date,return_date(Null=active loan).Relationships(M:1 Members si dhe M:1 Books)


Instalimi dhe konfigurimi:
<br>
1.pip install fastapi[all]
<br>
2.instalimi i Postgre SQL
<br>
3.pip install "psycopg[binary]"
<br>
4.pip install alembic
<br>
5.uvicorn app.main:app --reload (kjo e nis serverin)
<br>
6.pip install pytest
<br>
7.pip install httpx


Routers endpoints:
<br>
http://localhost:8000/docs
<br>
1.members.py CRUD(GET,POST,PUT,DELETE),
<br>
2.authors.py CRUD(GET,POST,PUT,DELETE),
<br>
3.categories.py CRUD(GET,POST,PUT,DELETE),
<br>
4.books.py CRUD(GET,POST,PUT,DELETE),
<br>
5.loans.py CRUD(GET,POST,PUT,DELETE),
<br>
6.books_py.py CRUD(GET,POST,PUT,DELETE),
<br>
7.reports.py me kqyr se cili member ka ma shume loans(limit 5)

Repository structure:
<br>
ReadMe.md ==>> Ne pika tshkurta projekti,
<br>
Reasoning ==> Ne pika te gjata projekti,
<br>
requirements.txt ==> Teknologjitë e Përdorura,
<br>
main.py ==> API routers,
<br>
models.py ==>> tabelat SQLAlchemy,
<br>
schemas.py ==> Pydantic schmas(BaseModel),
<br>
database.py ==>> lidhja me Postgre SQL,
<br>
alembic ==>> historiku i databazes,
<br>
tests ==>>pytest

Tek pytest ==>>  python -m pytest -v