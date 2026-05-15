Hapat qe i kom ndjek gjate zgjedhjes se detyres:

1.E kom kriju repositoryn

2.E kom hap ne visual edhe kom kriju file main.py ne kete rast interpreter u zgjedh python

3.E kom kriju nje virtual environment vent qe pas ksaj interpreter e kom zgedh vent (python.exe)

4.E kom instalu FastApi dhe uvicorn ne terminal (keto mka ra ma perpara mi perdore gjate ushtrimeve qe kam bere duke ndjek kursin ne Udemy)

5.E kom instalu edhe postman por prape e kom perdor uvicorn app.main:app --reload (ma praktik mu ka dok)

6.E kom instalu Postgre SQL eshte hera e pare qe e kom perdore edhe kjo u kon arsyeja pse mka shty me zgjedh detyren me Postgre SQL qe me msu diqka te re.U kon e lehte mu perdore por hera e pare pak ma veshtire derisa i msova qysh perdoret.

7.Krijimi i tabelave u kon i lehte (tek tabelat members,authors edhe categories)e ke shkrujt emrin e kolones pastaj data type e ke zgjedh edhe e ki specifiku Not NULL ose NULL(varesisht nga kerkesa) po ashtu edhe per primary key veq ke mujt me selektu. Kur ka vazhdu tek tabelat tjera(books,books_author,loans) qe kane pas foreign keys ka qen pak ma e veshtire derisa e kom pa te constraints mi shkrujt foreign keys me lidh me tabelen paraprake(ne kete rast books foriegn key e ka pas nga tabela categories,books_author i ka pas dy foreign_key qe ka qen hera e pare qe kom kriju nje tabel me composite PK si dhe tek loans jon perfshi keto dy foreign keys) po ashtu te pjesa e constraints u kon edhe pjesa qe u specifiku kur nje kolone u kon unique.

8.Ne visual i kom kriju krejt files dhe folders qe jon kon te kerkume ne detyre

9.E kom instalu Psycopg 3 i cili ka qen verzioni me i ri edhe kjo ma ka mundesu lidhjen ne mes te Python edhe Postgre SQL 

10.I kom kriju tabelat ne fillim te gjitha mandej kom vazhdu mi insertu te dhenat (4 tabela i kom insertu me te dhena ne databaze ndersa 2 tabela i kom insertu tek file seed.py).Dhe per tabela te dhenat qe i kom insertu i kom gjeneru me gemini

11.Ne fillim databazes ja kom lon emrin Book Library po nderkohe mka dal problem gjate lidhjes per ate arsye e kom ndrru emrin e databazes ne book_library ,po ashtu edhe emrat e tabelave i kom bo me shkronje te madhe per ate arsye "" u dasht mi perdore tek seed.py

12.E kom instalu alembic ne terminal e cila eshte nje database migration tool (ketu kom marr ndihme nga copilot per me instalu sepse ne terminal mdilshin disa errora qe vete smujsha mi zgjedh)

13.Tek main.py e kom importu FastApi e kom lidh me databaze edhe e kom kqyr a po muna mi marr te dhenat qe i kom insertu atje edhe databaza u lidh me sukses .

14.Kom vazhdu duke kriju schemas ne kete rast klasa me secilen tabel

15.Tek model.py kom kriju tabelat SQLAlchemy me te gjitha detajet qe i kom perfshi ne databaze

16.Ne fillim ne main.py e kom bo lidhjen me databaze pas analizimit te videos lidhjen me databaze e kom bo tek database.py ndersa tek main.py e kom lon vetem lidhjen me fastapi

17.Tek routers i kom kriju te gjitha files per secilin liber qe e kom kriju edhe me fillu mi kriju endpoints

18.Tek main.py e kom lon health endpoint si dhe i kom importu te gjitha endpoints tek folderi router permes app.include_router()

19.Kom fillu me krijimin e endpoints te cilat pi kontrolloj a po funksionojn pastaj po vazhdoj te tjetra.Keto pi boj me radh si tek detyra qysh jane te listuara Health endpoints,CRUDE(GET,POST,PATCH,DELETE),Loan operators,Hardendpoint-filtered,sorted,paginated book search si dhe reports.

20.Nderkohe gjate krijimit te endpoints po shikoj mos ka nevoj per ndonje korigjim sikur ne schema

21.Why DELETE on a member with active loans returns 409
Sepse nuk duhet me fshi nje member i cili ka met akoma pa e kthy librin

22.Menyra qysh kom shku me realizimin e enpoints i kom kry CRUD operators tek te gjithe files pastaj ne vazhdim i kom shtu endpoints te tjere te cilat kane qene required dhe po ashtu njekohesisht kom bo disa korigjime ne endpoints paraprak

23.Ne perfundim tek endpoints e kom kriju tek routers edhe nje file te ri per reports qe na ka kthy member qe ka pas me se shumti loans.

24.Si hap te fundit per perfundimin e detyres eshte testimi(pytest) tek folderi tests qe e kom kriju ne fillim dhe tash pi shtoj files te nevojshem per testim

25.Pas pergaditjes se file ne terminal e kom instalu pytest po ashtu edhe httpx e cila perdoret per me dergu http requests gjate pytest testimit ne FastAPI

26.Pas instalimit te httpx behet from fastapi.testclient import TestClient