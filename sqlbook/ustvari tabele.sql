-- Active: 1678317163634@@baza.fmf.uni-lj.si@5432@sem2023_lucijaf@public
CREATE TABLE recepti(  
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    st_porcij INTEGER,
    cas_priprave INTEGER,
    cas_kuhanja INTEGER,
    id_uporabnika INTEGER
);

CREATE TABLE sestavinereceptov(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    kolicina TEXT,
    enota TEXT,
    sestavina TEXT NOT NULL
);


CREATE TABLE postopki(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    st_koraka INTEGER NOT NULL,
    postopek TEXT NOT NULL
);

CREATE TABLE nutrientske_vrednosti(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    kalorije FLOAT,
    proteini FLOAT,
    ogljikovi_hidrati FLOAT,
    mascobe FLOAT
);

CREATE TABLE oznake(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    oznaka TEXT NOT NULL
);

CREATE TABLE kulinarike(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    kulinarika TEXT NOT NULL
);

CREATE TABLE kategorije(
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    kategorija TEXT NOT NULL
);

CREATE TABLE sestavine(
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    kalorije FLOAT,
    proteini FLOAT,
    ogljikovi_hidrati FLOAT,
    mascobe FLOAT
);


CREATE TABLE uporabnik(
    id SERIAL PRIMARY KEY,
    uporabnisko_ime TEXT NOT NULL,
    geslo TEXT NOT NULL UNIQUE,
    zadnji_login DATE
);

CREATE TABLE komentarji(
    id SERIAL PRIMARY KEY,
    id_uporabnika INTEGER NOT NULL REFERENCES uporabnik(id),
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    vsebina TEXT NOT NULL,
    datum_objave text NOT NULL
);

CREATE TABLE komentarji1(
    id SERIAL PRIMARY KEY,
    id_uporabnika INTEGER NOT NULL REFERENCES uporabnik(id),
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    vsebina TEXT NOT NULL
);

CREATE TABLE komentarji2(
    id SERIAL PRIMARY KEY,
    id_uporabnika INTEGER NOT NULL REFERENCES uporabnik(id),
    id_recepta INTEGER NOT NULL REFERENCES recepti(id),
    vsebina TEXT NOT NULL,
    datum_objave TIMESTAMP DEFAULT Now()
);

ALTER TABLE komentarji
ADD COLUMN id_recepta INTEGER NOT NULL REFERENCES recepti(id);

ALTER TABLE komentarji
ALTER COLUMN datum_objave SET DATA TYPE TEXT;

ALTER TABLE uporabniki
RENAME TO uporabnik;

ALTER TABLE recepti ADD COLUMN id_uporabnika INTEGER;
UPDATE recepti set id_uporabnika=0;

DROP TABLE komentarji;

select relation::regclass, * from pg_locks where not granted;

REVOKE CONNECT ON DATABASE sem2023_lucijaf FROM PUBLIC, lucijaf;

SELECT 
    pg_terminate_backend(pid) 
FROM 
    pg_stat_activity 
WHERE 
    -- don't kill my own connection!
    pid <> pg_backend_pid()
    -- don't kill the connections to other databases
    AND datname = 'database_name'
    ;

GRANT CONNECT ON DATABASE sem2023_lucijaf TO lucijaf;