# Kort oppgave i Python #


## Oppsumering: ##
Et lite api som er skrevet i Python med FastAPI(Backend rammeverk). 
Api-en bruker "https://code-challenge.stacc.dev//api/pep?name" for å utføre PEP sjekk, og legger til en slags form for access control.
Jeg bruker en MySQL database some inneholder inneholder en tabell med 2 kolonner: (token, remaining_api_calls). 
En bruker trenger en token for å få tillatelse til å utføre PEP sjekk.
For hver gang en bruker utfører en PEP sjekk så blir "remaining_api_calls" mindre.

## Installasjonskrav AWS ##
Jeg har deployet backend api og database med å bruke en AWS EC2 compute instance og en RDS MySQL database.
EC2 url: http://ec2-13-40-130-85.eu-west-2.compute.amazonaws.com/

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
## Installasjonskrav lokal PC ##
```
apt-get install python3.9
Python pakker: 
pip3 install fastapi
pip3 install "uvicorn"
pip3 install aiohttp[speedups]
pip3 install aiomysql
```
## Hvordan starte web server ##
Naviger til der hvor main.py befinner seg.
Kjør i terminal/cmd: uvicorn main:app --reload


## Database config ##
Databasen kjører på AWS. Jeg bruker følgende kode for å opprette en database og tabell, og lage 2 tokens.
```
CREATE DATABASE stacc_db;

USE stacc_db;

CREATE TABLE api_token (
	token VARCHAR(34) PRIMARY KEY,
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
GET /api/pep?name=Knut Arild Hareide &token=0xb9b09ebdf29f464s82e23269c535acbd HTTP/1.1
```
Viss token har tillatelse til å gjøre flere api calls, da er formatet på respons følgende:
```
{"status" : 1, "description" : "success", "response" : responsen fra eksisterende STACC api}
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
