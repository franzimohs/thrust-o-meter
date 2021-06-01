### Thrust-O-Meter

## Nutzungsanleitung


Schließe das Trainingsgerät via USB an den Computer an. 
Führe die Datei Thrust-O-Meter aus. 
Gebe den Port an. Er ist im Gerätemanager zu finden. 

Es stehen nun verschieden Funktionen zur Verfügung:

1. Aufnahme eines Impulses (AUFNAHME!)
2. Analyse eines aufgenommenen Impulses und Vergleich mit einem Referenzimpuls (ANALYSE! bzw. Freie Analyse!)
3. Visuelle Echtzeitausgabe (REALTIMEPLOT!)
4. Auditive Echtzeitausgabe (SOUND!) 
5. Spiel "Flappy Bone" (SPIEL!)
6. Anzeige des Lernfortschrittes (FORTSCHRITT!)
7. Eichung des Gerätes (Eichung 1kg Rechts und SAVE!)



# 1. Aufnahme eines Impulses (AUFNAHME!)

Links wird der Name der Datei angezeigt. Alle Dateien werden mit einem Zeitstempel benannt (JJJJMMDD_HHMMSS). 
Soll der Name geändert werden, bitte **unbedingt** unten *ohne Referenz* auswählen, da ansonsten das Programm Lernfortschritt
beschädigt werden kann!

Wähle die Seite, auf der der Impuls ausgeführt werden soll aus. Wähle die Referenz aus, mit der dein Impuls später verglichen
werden soll. Die Parameter des Impulses orientieren sich dabei an der Maximalkraft wie folgt:

Vorspannungskraft: 1/4 der Maximalkraft
Vorspannungslänge: kann in der Analyse später frei gewählt werden
Impulsdauer: 150ms

Möchtest du einen Impuls mit freien Parametern ausführen, wähle *ohne Referenz*. Dein Impuls wird in diesem Fall nicht in den 
Lernfortschritt mit aufgenommen. 

Drücke *start* um die Aufnahme zu starten. Führe nun deinen Impuls auf die Beckenschaufel aus. Richte den Vektor deines Impulses 
dabei möglichst entlang der Beckenschaufel aus. Drücke *stop&save* um den Impuls zu speichern. 
Er erscheint nun als Datei im Ordner *ausgabe*.

# 2. Analyse eines aufgenommenen Impulses und Vergleich mit einem Referenzimpuls (ANALYSE! bzw. Freie Analyse!)

Wähle mit dem Button *Browse* eine Datei aus dem Ordner *ausgabe* aus. Die Dateien sind nach Datum und Zeit der Aufnhame 
benannt (JJJJMMDD_HHMMSS). Die Endungen tom0, tom1, tom2, tom3 und tom4 verweisen auf die gewählte Impulsstärke. 

Gib nun die gewünschte Vorspannungslänge für den Referenzimpuls in das Feld *Vorspannungslänge* in Millisekunden ein (1s = 1000ms). 
Drücke nun den Button *ANALYSE!* um die Analyse zu starten. Dein Impuls wird dabei mit dem in der Aufnahmefunktion gewählten
Referenzimpuls verglichen. Alternativ kannst du alle Felder rechts des Buttons ausfüllen und mit dem so erzeugten Referenzimpuls eine 
*FREIE ANALYSE!* durchführen (Impulsdauer ist stets 150ms).

# 3. Visuelle Echtzeitausgabe (REALTIMEPLOT!)

Um deine Daten in Echtzeit anzuschauen drücke den Button *REALTIMEPLOT!*.
Hier kannst du einen Zielwert einstellen indem du die durchgängige Linie oben im Plot mit der Maus auf eine beliebige Höhe verschiebst.
Möglich sind werte zwischen 50N und 400N. 
Zusätzlich kannst du die Seite wechseln, welche angezeigt werden soll.
**Achtung:** die zu häufige Nutzung von visuellem Feedback in Echtzeit kann sich negativ auf den Lernerfolg auswirken. Nutze daher bitte 
vorrangig die Aufnahmefunktion oder die auditive Echtzeitausgabe.

# 4. Auditive Echtzeitausgabe (SOUND!)

Um die Auditive Echtzeitausgabe zu starten, drücke den Button *SOUND!*.
Drücke auf *START!* damit die Ausgabe beginnt. Du hörst nun einen Durchgängigen Ton. Die Tonhöhe verändert sich je nach Stärke der 
ausgeübten Kraft. Auch hier kannst du die Seite auswählen, welche du benutzen möchtest. Drücke *STOP!* um den Ton anzuhalten. 
Sollte der Ton von selbst aufhören, drücke erneut auf *START!*. 

# 5. Spiel "Flappy Bone" (SPIEL!)

Wähle zunächst die Seite aus, mit welcher du spielen möchtest. Um das Spiel "Flappy Bone" zu starten, drücke auf *SPIEL!*. 
Du siehst nun den Startbildschirm des Spiels. Betätige die Leertaste oder drücke auf die gewählte Seite des Trainingsgerätes 
um zu starten. Je nach Stärke der ausgeüben Kraft steigt der flatternde Knochen nach oben. Weiche den Röhren aus und setze 
schnelle Impulse um die Knochen am oberen Bildschirmrand zu berühren. Wenn ein Knochen verpasst wird, gibt es keinen Schaden.
Nach jeweils 10 erreichten Punkten wird das Spiel etwas schneller. 

# 6. Anzeige des Lernfortschrittes (FORTSCHRITT!)

Drücke den Button *FORTSCHRITT!* um die Zusammenfassung aller aufgenommenen Impulse zu sehen. Hierbei wird auf der Y-Achse jeweils die Abweichung des 
Parameters von der bei der Aufnahme gewählten Referenz angezeigt. Die X-Achse zeigt die Nummer des Impulses nach Aufnahmedatum.
Mit zunehmendem Lernfortschritt sollte sich der Graph also an die Nulllinie annähern. 

# 7. Eichung des Gerätes (Eichung 1kg Rechts und SAVE!)

Um das Gerät zu eichen bestehen zwei Möglichkeiten. 
1. Das Gerät wurde bereits geeicht und wird nun mit einem neuen Gerät genutzt: Frage die Person, welche das Gerät geeicht hat nach den aktuellen Werten.
Füge diese in die Felder links neben dem Button *Eichung 1kg rechts* ein und drücke direkt auf *SAVE!*.

2. Das Gerät wurde neu gebaut, oder verändert und muss neu geeicht werden: Lege ein Massestück von 1kg auf die rechte Beckenseite. 
Achte darauf, dass das Massestück möglichst nur auf der Beckenschaufel aufliegt. Drücke nun den Button *Eichung 1kg rechts*. Lege
das Massestück nun auf die linke Seite des Beckens. Drücke den Button *Eichung 1kg links*. Drücke nun den Button *SAVE!*. 


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Lizenzvertrag" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Dieses Werk ist lizenziert unter einer <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Namensnennung - Nicht-kommerziell - Weitergabe unter gleichen Bedingungen 4.0 International Lizenz</a>.

**Die Nutzung zu Lehrzwecken ist ausdrücklich erlaubt!**

**CC Franziska Mohs, 2021**


## Abhängigkeiten(Python)

Thrust-O-Meter basiert auf folgenden Bibliotheken:

* [pygame](https://github.com/pygame/)
* [aupyom](https://github.com/pierre-rouanet/aupyom)
* [numpy](https://github.com/numpy/numpy)
* [scipy](https://github.com/scipy/scipy)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph)
* [pyserial](https://github.com/pyserial/pyserial)