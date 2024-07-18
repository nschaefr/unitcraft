# Unitcraft
Unitcraft ist ein Python-Kommandozeilentool, welches im Rahmen meiner Bachelorarbeit zum Thema: <br><br>
**Sind Sprachmodelle in der Lage die Arbeit von Software-Testern zu übernehmen?
<br> Automatisierte JUnit Testgenerierung durch Large Language Models**

entstanden ist. Es dient zur automatischen Generierung von JUnit5 Tests in Java-Maven Projekten. Da der Fokus auf der Qualitätsmessung des Sprachmodells *GPT-4o* liegt, wird das Ergebnis (der generierte Testcode) ohne manuellen Einfluss oder Verfeinerung durch Extra-Funktionalitäten übernommen.

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
Das Tool wird im *root*-Verzeichnis deines Projektes mit folgendem Befehl gestartet:

```bash
python3 path/to/main.py
```



