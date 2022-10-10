# Kort oppgave i Python / kode innlevering #


## Oppsumering: ##
Et lite API som er skrevet i Python med FastAPI (Backend rammeverk). 
API-en bruker "https://code-challenge.stacc.dev/api/pep?name" for å utføre PEP sjekk, og legger til en token-basert access control for å begrense hvor mange api calls en bruker kan gjøre. Jeg bruker en MySQL database some inneholder en tabell med 2 kolonner: (token, remaining_api_calls). 
En bruker trenger en token for å få tillatelse til å utføre PEP sjekk.
For hver gang en bruker utfører en PEP sjekk så blir "remaining_api_calls" mindre. Viss "remaining_api_calls" er 0, da vil det ikke være mulig å gjøre flere PEP sjekk.
Jeg har forsøkt å publisert backend api + database ved bruk av AWS. Se 2 seperate beskrivelser for installasjon på lokal PC og AWS. 
## Installasjonskrav ##
### Installasjonskrav AWS ###
Jeg har deployet backend api og database med å bruke en AWS EC2 compute instance og en RDS MySQL database.
- EC2 url: http://ec2-13-40-130-85.eu-west-2.compute.amazonaws.com/
- For noe interaktiv bruk av api, se http://ec2-13-40-130-85.eu-west-2.compute.amazonaws.com/docs/

For Amazon Linux 2, kernel 5.10 bruker jeg følgende kommandoer for å installere og starte opp backend server.
```
yum -y install git
yum -y install python3
pip3 install fastapi
pip3 install "uvicorn[standard]"
pip3 install aiohttp[speedups]
pip3 install aiomysql

git clone https://github.com/bragebja/stacc-oppgave.git
cd stacc-oppgave
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000
nohup uvicorn main:app --reload --host 0.0.0.0 &
```
### Installasjonskrav lokal PC (Linux) ###
```
apt-get install python3.9
pip3 install fastapi
pip3 install "uvicorn"
pip3 install aiohttp[speedups]
pip3 install aiomysql
```
### Hvordan starte web server lokalt ###
```
git clone https://github.com/bragebja/stacc-oppgave.git
cd stacc-oppgave
```
I filen database.py, endre følgende:
```
HOST = "database-1eu.cobpbett9lnf.eu-west-2.rds.amazonaws.com"
```
til:
```
HOST = "database-2.c2z77t0mvtlc.us-east-1.rds.amazonaws.com"
```
Naviger til der hvor main.py befinner seg.

Kjør i terminal/cmd: uvicorn main:app --reload

API vil være tilgjengelig på http://127.0.0.1:8000/api

For noe interaktiv bruk av api, se http://127.0.0.1:8000/docs


## Database config ##
Databasen kjører på AWS. Jeg bruker følgende kode for å opprette en database og tabell, og lage 2 tokens.
```
CREATE DATABASE stacc_db;

USE stacc_db;

CREATE TABLE api_token (
	token VARCHAR(32) PRIMARY KEY,
    remaining_api_calls INT
);

INSERT INTO api_token (token, remaining_api_calls) values 
("b90d09ebdf29f46482e23269c5356fe3", 0),
("b9b09ebdf29f464s82e23269c535acbd", 1000);
```

## API endpoints ##

### pep ###
PEP endpoint ligner på tilsvarende endpoint fra https://code-challenge.stacc.dev/. Forskjellen er at det kreves en token som parameter, og responsen er litt annerledes.
```
GET /api/pep?name=Knut Arild Hareide &token=b9b09ebdf29f464s82e23269c535acbd HTTP/1.1
```
Viss token har tillatelse til å gjøre flere api calls, da er formatet på respons følgende:
```
{"status" : 1, "description" : "success", "response" : responsen fra eksisterende STACC api}
```
Viss token ikke har tillatelse, eller ikke eksisterer, da ser formatet slik ut:
```
{"status": 0, "description": "Key has no remaining api calls or does not exist", "response": {} }
```

### api_token ###
api_token endpoint kan brukes for å generere en token med tillatelse til å utføre 100 api calls / pep calls. En request ser slik ut:
```
POST /api/api_token HTTP/1.1
```
En response kan se slik ut:
```
{"status" : 1, "description" : "Success", "token" : b9b09ebdf29f464s82e23269c535acbd}
```
Eller feks slik ut:
```
{"status" : 0, "description" : "Something went wrong"}
```

### remaining_api_calls ###
remaining_api_calls kan brukes for å sjekke hvor mange api calls en token har igjen. En request ser slik ut:
```
POST /api/remaining_api_calls?token=b9b09ebdf29f464s82e23269c535acbd HTTP/1.1
```
En respons kan se slik ut:
```
{"status" : 1, "description" : "Success", "remaining_api_calls" : 30}
```
Eller feks:
```
{"status" : 0, "description" : "Token does not exist"}
```

## Kommentarer ##
- For å gjøre ting litt enkelt har jeg valgt å inkludere token som et parameter, slik at det feks er enklere å teste. Det hadde nok sikkert vært bedre å brukt cookies eller lignende for dette.

- Det er mulig å generere nye tokens hele tiden. Dette er i hovedsak gjort bare for å illustrere en enkel måte å genere token på / gjøre database query.

- Se bortifra svak database passord, og passord i codebase. Dette er også noe som er gjort for enkelt skyld, til tross for svak sikkerhet.
