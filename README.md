# Database-System-with-Meteorological-Data-API-REST-
Cerinta: Realizarea unui sistem de stocare intr-o baza de date a unor date meteorologice. Acest sistem are la baza un API REST.

Detalii de functionare:

S-a pornit de la ideea formarii a 3 containere folosind Docker Compose:
1. un container ce contine baza de date (image: postgres) - baza de date folosita de mine este PostgreSQL
2. un container pentru utilizarea bazei de date (image: dpage/pgadmin4) - pentru o interfata usor de controlat am ales pgAdmin4
3. un container destinat server-ului (document ce contine colectia de rute implementate sa raspunda cerintelor) - implementarea s-a realizat in Python cu ajutorul framework-ului web Flask si a lui SQLAlchemy.

Serverul mentionat la punctul 3 se gaseste in folderul src alaturi de Dockerfile-ul necesar crearii containerului, iar fisierul requirements.txt contine sinteza tuturor bibliotecilor si versiunilor de biblioteci folosite in realizarea serverului, ce sunt instalate ulterior in Dockerfile. 

Pentru baza de date toate credentialele se gasesc in environmentul din fisierul pentru Docker Compose - docker.yml care se gaseste in afara folder-ului src. Mentionez ca in cazul acestui container s-a dorit si crearea unui volum, dar din motive inca neintelese de incopatibilitate a lui SQLAlchemy, server-ul cadea atunci cand faceam configuratiile necesare.

Utilitarul de gestiune ales a configurat la instalare un username si o parola care au fost introduse in acelasi fisier mentionat anterior.


Descrierea rutelor implementate:

Fiecare ruta a fost tratata separat, iar raspunsurile au corespuns fie unui mesaj de succes si a unor date, fie unui cod de eroare.

S-au folosit clase si contructori pentru definirea si initializarea tabelelor in care au fost puse datele in functie de cele trei categorii: Countries, Cities si Temperatures.

Pentru rutele de la Countries s-a verificat daca fisierul de test contine datele necesare adaugarii/modificarii unei inregistrari, iar in cazul in care acestea nu existau s-a intors eroarea 400 BAD REQUEST. In cazul rutelor cu id in calea data s-a verificat existenta id-ului in baza de date si apoi au fost facute modificari asupra inregistrarii. S-a intors eroarea 409 in cazul in care exista un conflict in baza de date (spre exemplu: adaugarea de doua ori a unei tari cu acelasi nume).

Pentru rutele de la Cities au fost respectate toate cele dezvoltate anterior la Countries. Au fost setate constrangeri de cheie straina pentru ca stergerile si modificarile sa aiba loc in cascada, evitandu-se astfel situatiile in care un oras sa contina un id de tara care nu exista.

Pentru rutele de la Temperatures au fost preluate datele din URL si apoi s-au facut verificarile de rigoare pentru intoarcerea datelor din get. A fost tratat cazul in care ruta primeste toate cele 4 argumente, dar si cazul in care nu primeste niciunul (pentru GET/api/temperatures?lat=Double&lon=Double&from=Date&until=Date). Si aici au fost impuse constrangeri in ceea ce priveste id-ul orasului care este corespunzator unei valori a unei temperaturi. 
 

Testarea s-a rezalizat cu ajutorul fisierului de test (TestAPI-Tema2_v2) pus la dispozitie, iar pentru rularea testelor din cadrul fisierului s-a folosit aplicatia Postman.
