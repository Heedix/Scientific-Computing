# Scientific Computing mit JupyterLab und Docker

Ein deutschsprachiges Starterprojekt entlang deiner achtteiligen Kursübersicht.

- `notebooks/01_Scientific_Computing.ipynb`: Erklärungen, ausführbare Beispiele und Übungen zu allen acht Themenblöcken.
- `notebooks/02_Bash_und_Werkzeuge.ipynb`: zweiter Sprachkernel, MPI mit Python und C, Maxima, GP und die PARI-C-Bibliothek.
- `examples/`: kleine eigenständige Python- und C-Programme.

## Start auf Windows

1. **Docker Desktop starten** und warten, bis die Engine läuft. Die Umgebung verwendet **Linux-Container**, auf Windows üblicherweise mit WSL 2. Falls nötig: [Docker-Desktop-Installation](https://docs.docker.com/desktop/setup/install/windows-install/).
2. Öffne PowerShell im Ordner `scientific-computing`, also dort, wo `compose.yaml` liegt. Bei einem ZIP zuerst **alles entpacken**.
3. Führe aus:

```powershell
docker compose up --build
```

Beim ersten Mal werden das Basisimage, Linux-Werkzeuge und Python-Pakete heruntergeladen. Das benötigt Internetzugriff, Zeit und freien Speicher. Die späteren Starts verwenden das gebaute Image:

```powershell
docker compose up
```

4. Öffne [JupyterLab](http://localhost:8888/lab). Mit dieser lokalen Compose-Konfiguration brauchst du weder ein Konto noch einen Token oder ein Passwort.
5. Öffne links `notebooks/01_Scientific_Computing.ipynb`. Wähle **Python 3 (Scientific Computing)** und führe die erste Zelle mit **Shift+Enter** aus.

Das klassische Notebook-Frontend findest du unter [localhost:8888/tree](http://localhost:8888/tree).
Für das zweite Notebook **Bash** auswählen. Ein Kernelwechsel verändert die Sprache des vorhandenen Codes nicht.

## Was installiert ist

| Bestandteil | Verwendung |
|---|---|
| Python 3.12, JupyterLab, Jupyter Notebook | Lernumgebung |
| NumPy, SymPy, Matplotlib, SciPy | Numerik, symbolisches Rechnen, Diagramme, Interpolation |
| Open MPI, mpi4py, C-Compiler | Parallele Programme mit Python und C |
| Maxima | Symbolische Algebra als externes Programm |
| PARI/GP und PARI-Entwicklungsbibliothek | Zahlentheorie über GP-Shell und C |
| Python- und Bash-Kernel | Zwei direkt nutzbare Jupyter-Kernel |

Für Maxima verwendet das Image die [Debian-Variante mit ECL](https://packages.debian.org/bookworm/maxima-sage), erreichbar als `maxima`. Der Paketname `maxima-sage` bedeutet dabei nicht, dass das vollständige SageMath installiert wird.

SageMath wird im Notebook eingeführt, ist wegen seines Umfangs aber separat einzurichten.
Maple und MATLAB sind ebenfalls nicht mitgeliefert; deren Nutzung benötigt eigene Installationen und passende Lizenzen.
Das Notebook verlinkt die jeweiligen offiziellen Anleitungen und unterscheidet Bibliotheksanbindung, Prozessaufruf und Sprachkernel.

## Speichern und Beenden

Die lokalen Ordner `notebooks` und `examples` sind eingebunden. Dort gespeicherte Dateien bleiben nach `docker compose down` erhalten. Dateien an anderen Stellen im Container sind nicht entsprechend gesichert.

In Jupyter mit **Strg+S** speichern. Zum Beenden im Startterminal **Strg+C**, danach gegebenenfalls:

```powershell
docker compose down
```

Im Hintergrund starten und Logs ansehen:

```powershell
docker compose up -d
docker compose logs jupyter
```

Der Dienst ist nur über `127.0.0.1` veröffentlicht. Die Token- und Passwort-Anmeldung sind für diese lokale Nutzung deaktiviert; lokale Programme und andere Benutzer deines Rechners können den Dienst dadurch ebenfalls erreichen. Diese Einstellung nur auf deinem eigenen, vertrauenswürdigen Rechner verwenden und den Port nicht für das Netzwerk freigeben.

Nach einem Wechsel von der bisherigen Konfiguration mit Token zuerst die Notebooks speichern, dann den Container neu erstellen:

```powershell
docker compose up -d --force-recreate
```

Ein erneuter Image-Build ist dafür nicht nötig. Zum Wiederaktivieren der Anmeldung die beiden Einträge `--IdentityProvider.token=` und `--PasswordIdentityProvider.hashed_password=` unter `command` in `compose.yaml` entfernen und den Container erneut erstellen.

## Umgebung und beide Notebooks prüfen

Bei der Erstellung wurden Notebook-JSON, Python-Syntax, Compose-Konfiguration und ausgewählte numerische Zellen erfolgreich geprüft, einschließlich Newton-Konvergenz, Fehlerfällen und linearen Gleichungssystemen. Ein vollständiger Container-Build und die Ausführung beider Notebooks waren hier wegen fehlender Zugriffsrechte auf die Docker-Schnittstelle nicht möglich. Die MPI-, CAS- und Bash-Laufzeitprüfung steht daher noch aus.

Bei laufendem Dienst:

```powershell
docker compose exec jupyter python scripts/check_environment.py
```

Der Check prüft Imports, Werkzeuge und Kernel, startet MPI mit einem und drei Prozessen und führt beide Notebooks mit frischen Kerneln aus. Das Python-Notebook prüft zusätzlich MPI mit vier Prozessen, kompiliert C-Beispiele und berechnet mathematische Beispiele samt Residuen. Die ausgeführten Notebooks werden mit der Endung `_executed.ipynb` gespeichert; die Quelldateien bleiben erhalten.

Alternativ ohne dauerhaft laufenden Jupyter-Server:

```powershell
docker compose build
docker compose run --rm jupyter python scripts/check_environment.py
```

## Kleine Probleme selbst lösen

| Problem | Lösung |
|---|---|
| `docker` wird nicht erkannt | Docker Desktop installieren; PowerShell neu öffnen. |
| `dockerDesktopLinuxEngine` / Verbindung zur Engine fehlt | Docker Desktop starten und auf die laufende Linux-Engine warten. |
| Port 8888 ist belegt | In einer Datei `.env` neben `compose.yaml` die Zeile `JUPYTER_PORT=8890` speichern. Danach `docker compose up -d` und `http://localhost:8890/lab` öffnen. |
| Es erscheint weiterhin die Jupyter-Anmeldung | Geänderte `compose.yaml` verwenden, Notebooks speichern und `docker compose up -d --force-recreate` ausführen. Danach `http://localhost:8888/lab` ohne alten Token-Link öffnen. |
| `ModuleNotFoundError` | Prüfen, ob du den Python-Kernel dieses Containers verwendest; nach Änderungen an `requirements.txt` neu bauen. |
| Ergebnisse passen nicht zum Code | Speichern, dann **Run → Restart Kernel and Run All Cells**. |
| MPI-Ausgaben haben andere Reihenfolge | Erwartbar: Prozesse schreiben unabhängig voneinander. |

## Erweiterungen und Versionen

Pakete für dauerhafte Ergänzungen in `requirements.txt` eintragen und `docker compose up --build` ausführen.
Eine Installation nur im laufenden Container kann beim Neuerstellen verloren gehen.

Das Projekt verwendet kompatible Versionsbereiche und ein Python-Basisimage mit Tag. Neue Builds können dadurch andere Paketstände erhalten. Die erste Notebook-Zelle zeigt die aufgelösten Versionen. Für einen Kurs mit festem Stand nach erfolgreichem Build einen Paket-Snapshot exportieren:

```powershell
docker compose exec -T jupyter python -m pip freeze | Set-Content -Encoding utf8 requirements-resolved.txt
```

Für genauere Reproduzierbarkeit zusätzlich das gebaute Image archivieren oder dessen Digest festhalten; der Pip-Snapshot alleine fixiert weder Linux-Pakete noch das Basisimage.

## Offizielle Quellen

- [Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Jupyter-Server-Anmeldung](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
- [Bash-Kernel](https://github.com/takluyver/bash_kernel)
- [mpi4py-Installation](https://mpi4py.github.io/mpi4py/stable/html/install.html)
- [mpi4py-Tutorial](https://mpi4py.github.io/mpi4py/stable/html/tutorial.html)

Weitere Dokumentation zu Python, den Mathematikbibliotheken und Computeralgebrasystemen steht am Ende des Hauptnotebooks.
