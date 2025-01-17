> # Werkplaats 2: Test Correct applicatie project

---

## Team: 
Error not found (1E3)
* Anmol Haribhajan (1096493)
* Ihssane El Bahraoui (1103386)
* Jordi Vrolijk (1111805)
* Julie Blokland (1010439)
* Yoshua Volkerts (1045100)
* Askari Sardar (1112079)

### Installation & venv files:

#### Benodigdheden:
* Python/Pycharm versie 2024.3.3.1
* Installeer een nieuwe venv stappen doornemen
* Installeer de pakketten in de requirements.txt file via bash command: pip install -r requirements.txt
* Creëer een nieuwe Run/Debug Configuration

* Het is niet gelukt om via Git de virtual environment mee te geven
* Git laat deze niet uploaden en de bestanden blijven oranje

#### Installeren via Bash:

Venv file


Run/Debug Configuration


#### Handmatig:

Venv file
* rechts onderin zie je de current virtual environment file
* klik op: Add new interpreter (add local interpreter)
* Pak de eerste: Virtualenv Environment
* Klik op new, meeste staat al klaar, mocht je het in een andere map willen plaatsen 'bladeren'
* Klik dan op ok

Run/Debug Configuration
* Voordat je een Run/Debug aanmaakt, zorg dat je een virtual environment file hebt
* Rechts bovenin zie je Current file staan of 3 puntjes en edit
* Klap deze open en klik op edit configurations
* Klik op + en voeg een Flask server toe
* Zet deze op je aangemaakte virtual environment
* Mocht je nog een working directory willen toevoegen, kies dan de huidige project
* Klik dan op ok
* Met deze Flask configuratie kun je App.py starten (eerst de packages installeren op je venv)

pip install -r requirements.txt

Klik op onderstaande command en plak het in je terminal:

    [![Install Requirements](https://img.shields.io/badge/Install%20Requirements-%F0%9F%96%A5%20Click%20to%20copy-blue)](#requirements-command)

    **Command:**
    ```bash
    pip install -r requirements.txt
    ```

---

### Guide:
[Guide](markdown_files/guide.md)

---

### Clone the repository to your local machine:
git clone https://github.com/Rac-Software-Development/wp2-2024-mvc-1e3-error-not-found

---

### Website features:
* Inlog scherm
* Welkom scherm
* Toetsvragen
* Redacteuren (admin only)
* Redacteur toevoegen (admin only)
* Redacteur wijzigen/verwijderen (admin only)
* Ai prompts
* AI details 
* AI verwijderen (admin only)
* Ai prompt toevoegen (admin only)
* Nieuwe prompt toevoegen (admin only)
* Indexeren van taxonomie
* Resultaat van taxonomie (meerdere taxonomie opties)
* Wijzigen van taxonomie

---

### Credits: 
* Programming: Team: error not found
* Anmol Haribhajan, Ihssane El Bahraoui, Jordi Vrolijk, Julie Blokland, Yoshua Volkerts
* Hogeschool Rotterdam: leraren, lessen, powerpoints, workshops & opdrachten

---

### Sources & references:
[Bronnenlijst & verwijzingen](markdown_files/bronnenlijst.md)

---

### Screenshots

---









































# WP2 Starter 

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db)database met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.   
- Een [voorbeeld uitwerking](voorbeeld_uitwerking/app.py) van het meest complexe deel van de opdracht
