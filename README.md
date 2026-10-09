# csvstat

`csvstat` ist ein schlankes Kommandozeilen-Werkzeug in Python, das eine
CSV-Datei einliest und je Spalte Kennzahlen ausgibt: für numerische Spalten
`count`, `min`, `max`, Mittelwert und die Anzahl fehlender Werte, für Textspalten
die Anzahl eindeutiger Werte. Die Auswahl der Spalten steuerbar über `--columns`,
das Trennzeichen über `--delimiter`, und die Ausgabe auf Wunsch als JSON über
`--json`. Fehlende, leere oder datenzeilenlose Dateien werden mit einer
verständlichen Fehlermeldung auf `stderr` und einem Exit-Code ungleich 0
abgelehnt.

## Tech Stack

- **Sprache:** Python 3.11+
- **Laufzeit / CLI:** `argparse`
- **Abhängigkeiten:** nur die Standardbibliothek (`argparse`, `csv`, `json`, `statistics`)
- **Tests:** `pytest`
- **Plattform:** keine (reines CLI-Werkzeug)

## Installation

```bash
pip install -e .
```

Für die Tests zusätzlich:

```bash
pip install -e ".[test]"
```

## Verwendung

```bash
python -m csvstat DATEI
```

Nach der Installation steht auch der Konsolen-Befehl `csvstat` zur Verfügung:

```bash
csvstat DATEI
```

### Optionen

| Option | Bedeutung |
| --- | --- |
| `DATEI` | Pflichtangabe: die zu analysierende CSV-Datei. |
| `--delimiter Z` | Feldtrennzeichen, genau ein Zeichen (Standard: `,`). |
| `--columns a,b` | Kommagetrennte Liste der Spalten, die ausgewertet werden (Standard: alle). |
| `--json` | Gibt den Bericht als JSON statt als Klartext aus. |
| `--help` | Zeigt die Hilfe der Optionen an und beendet mit Exit-Code 0. |

### Beispiele

```bash
# Alle Spalten einer kommagetrennten Datei auswerten
python -m csvstat daten.csv

# Semikolongetrennte Datei, nur zwei Spalten, Ausgabe als JSON
python -m csvstat --delimiter ";" --columns name,alter --json daten.csv
```

Die Ausgabe erfolgt ausschließlich auf `stdout` (Bericht) bzw. `stderr`
(Fehlermeldungen). Es werden keine Ausgabedateien, Logdateien oder
Zwischendateien geschrieben, und es wird keine Netzwerkverbindung aufgebaut.

## Fehlerverhalten

Bei einer nicht existierenden, einer leeren oder einer Datei ohne Datenzeilen
gibt das Werkzeug eine Meldung der Form `csvstat: <Dateiname>: <Ursache>` auf
`stderr` aus und beendet sich mit einem Exit-Code ungleich 0. Die Meldungen
enthalten niemals Zellinhalte oder Zeilen aus der Eingabedatei, sondern nur den
Dateinamen, den Spaltennamen und die Fehlerursache.

## Tests

```bash
python -m pytest
```

## Funktionen (Feature-Liste)

- Einlesen einer CSV-Datei über `csv.reader` (erste Zeile = Kopfzeile).
- Einstellbares Trennzeichen (`--delimiter`).
- Spaltenauswahl (`--columns`).
- Kennzahlen je Spalte: numerisch `count`, `min`, `max`, Mittelwert, fehlende
  Werte; textuell die Anzahl eindeutiger Werte.
- Ausgabe als Klartext oder JSON (`--json`).
- Verständliche Fehlermeldungen für fehlende, leere und datenzeilenlose Dateien.
