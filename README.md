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

#### Benodigdheden (zie installeren):
* Python/Pycharm versie 2024.3.3.1
* Installeer een nieuwe venv stappen doornemen
* Installeer de pakketten in de requirements.txt file via bash command: pip install -r requirements.txt
* Creëer een nieuwe Run/Debug Configuration  

* Het is niet gelukt om via Git de virtual environment mee te geven
* Git laat deze niet uploaden en de bestanden blijven oranje

#### Installeren via Bash:

---

Venv file
Stap 1: Navigeer naar de gewenste map
Gebruik cd om naar de map te gaan waar je de virtuele omgeving wilt maken:

       cd /pad/naar/jouw/project

---

Stap 2: Creëer de virtuele omgeving
Gebruik het python of python3 commando om de virtuele omgeving te maken:

       python3 -m venv naam_van_venv

Vervang naam_van_venv met de gewenste naam voor je virtuele omgeving, bijvoorbeeld venv.

---

Stap 3: Activeer de virtuele omgeving
Afhankelijk van je shell (bijv. bash), gebruik je het volgende commando om de virtuele omgeving te activeren:

       source naam_van_venv/bin/activate

Je zult zien dat de prompt verandert en de naam van je virtuele omgeving toont, zoals:

       (venv) user@computer:~/project$

---

Stap 4: Deactiveer de virtuele omgeving
Als je klaar bent, kun je de virtuele omgeving deactiveren met:

       deactivate

---

Stap 5: Controleer of het werkt
Controleer of je in de virtuele omgeving zit door het volgende commando uit te voeren:

       which python

Dit zou naar het python-bestand in de venv-map moeten verwijzen, bijvoorbeeld:

       /pad/naar/project/venv/bin/python

---

Run/Debug Configuration
Stap 1: Maak een .idea map aan
PyCharm slaat configuraties op in een .idea map. Zorg dat deze aanwezig is:

     mkdir -p .idea/runConfigurations

---

Stap 2: Maak een XML-bestand voor de configuratie
Creëer een bestand zoals MyScript.xml:

     touch .idea/runConfigurations/MyScript.xml

---

Stap 3: Vul het bestand met een configuratie
Gebruik de volgende Bash-opdracht:

        cat <<EOL > .idea/runConfigurations/MyScript.xml
        <component name="ProjectRunConfigurationManager">
          <configuration default="false" name="MyScript" type="PythonConfigurationType" factoryName="Python">
            <module name="MyProject" />
            <option name="SCRIPT_NAME" value="\$PROJECT_DIR$/main.py" />
            <option name="WORKING_DIRECTORY" value="\$PROJECT_DIR$" />
            <option name="INTERPRETER_OPTIONS" value="" />
            <option name="PARENT_ENVS" value="true" />
            <envs />
            <option name="SDK_HOME" value="\$PROJECT_DIR$/venv/bin/python" />
            <option name="PARAMETERS" value="" />
            <method v="2" />
          </configuration>
        </component>
        EOL

Hiermee stel je een Run-configuratie in voor een script genaamd main.py.

---

#### Handmatig installeren:

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

#### Packages installeren:

      pip install -r requirements.txt

* Klik op onderstaande command en plak het in je terminal:

    [![Install Requirements](https://img.shields.io/badge/Install%20Requirements-%F0%9F%96%A5%20Click%20to%20copy-blue)](#requirements-command)

    **Command:**
    ```bash
  
    pip install -r requirements.txt
    ```

* Dit installeert alle benodigde packages

---

### Guide:
[Guide, stapsgewijs uitgelegd](markdown_files/guide.md)

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
