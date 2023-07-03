-- Active: 1678317163634@@baza.fmf.uni-lj.si@5432@sem2023_lucijaf@


-- dovolimo povezavo in uporabo scheme public javnosti
GRANT CONNECT ON DATABASE sem2023_lucijaf TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;

-- dovolimo vse nekemu konkretnemu uporabniku (WITH GRANT option, dovoli uporabniku dovoljevati pravice)
GRANT ALL ON DATABASE sem2023_lucijaf TO laran WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO laran WITH GRANT OPTION;

-- po ustvarjanju tabel
GRANT ALL ON ALL TABLES IN SCHEMA public TO lucijaf WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO laran WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO lucijaf WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO laran WITH GRANT OPTION;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;


-- Dodatne pravice za uporabo aplikacije

GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;

GRANT INSERT ON kategorije TO javnost;
GRANT INSERT ON komentarji2 TO javnost;
GRANT INSERT ON kulinarike TO javnost;
GRANT INSERT ON nutrientskevrednosti TO javnost;
GRANT INSERT ON oznake TO javnost;
GRANT INSERT ON postopki TO javnost;
GRANT INSERT ON recepti TO javnost;
GRANT INSERT ON sestavine TO javnost;
GRANT INSERT ON sestavinereceptov TO javnost;
GRANT INSERT ON uporabnik TO javnost;


GRANT DELETE ON kategorije TO javnost;
GRANT DELETE ON komentarji2 TO javnost;
GRANT DELETE ON kulinarike TO javnost;
GRANT DELETE ON nutrientskevrednosti TO javnost;
GRANT DELETE ON oznake TO javnost;
GRANT DELETE ON postopki TO javnost;
GRANT DELETE ON recepti TO javnost;
GRANT DELETE ON sestavine TO javnost;
GRANT DELETE ON sestavinereceptov TO javnost;
GRANT DELETE ON uporabnik TO javnost;

GRANT UPDATE ON kategorije TO javnost;
GRANT UPDATE ON komentarji2 TO javnost;
GRANT UPDATE ON kulinarike TO javnost;
GRANT UPDATE ON nutrientskevrednosti TO javnost;
GRANT UPDATE ON oznake TO javnost;
GRANT UPDATE ON postopki TO javnost;
GRANT UPDATE ON recepti TO javnost;
GRANT UPDATE ON sestavine TO javnost;
GRANT UPDATE ON sestavinereceptov TO javnost;
GRANT UPDATE ON uporabnik TO javnost;



GRANT ALL ON uporabnik TO lucijaf WITH GRANT OPTION;
GRANT ALL ON uporabnik TO laran WITH GRANT OPTION;
GRANT ALL ON uporabnik TO javnost WITH GRANT OPTION;