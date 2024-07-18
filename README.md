# Unitcraft
Unitcraft ist ein Python-Kommandozeilentool, welches im Rahmen meiner Bachelorarbeit zum Thema: <br><br>
**Sind Sprachmodelle in der Lage die Arbeit von Software-Testern zu übernehmen?
<br> Automatisierte JUnit Testgenerierung durch Large Language Models**

entstanden ist. Es dient zur automatischen Generierung von JUnit5 Tests in Java-Maven Projekten. Da der Fokus auf der Qualitätsmessung des Sprachmodells *GPT-4o* liegt, wird das Ergebnis (der generierte Testcode) ohne manuellen Einfluss oder Verfeinerung durch Extra-Funktionalitäten übernommen.<br><br>
Folgende Funktionalitäten werden bereitgestellt:
* Nutzerabfrage zum Initialisieren der Prompt- und Temperaturvariablen
* Automatisches Erfassen aller Java Klassen
* Erstellen eines Prompts
* Generieren von Testcode über API-Anfrage zur Kommunikation mit dem LLM
* Überprüfung der Kompilierbarkeit der Testklasse
* Repair Rounds zur Fehlerbehebung oder zum Löschen relevanter Codeausschnitte/der Testklasse
* Schreiben der Testklasse in Java-Datei sowie Ablegen im test-Verzeichnis mit korrektem Pfad

Das Projekt sollte folgende Struktur aufweisen und einen leeren *test*-Ordner besitzen:

```
project
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
```
Zusätzlich ist das Anlegen einer *.env* notwendig, in welcher der OpenAI-API Key als String in einer Variablen *OPEN_API_KEY* gespeichert wird.<br><br>
Das Tool wird im *root*-Verzeichnis des Projektes mit folgendem Befehl gestartet:

```bash
python3 path/to/main.py
```



