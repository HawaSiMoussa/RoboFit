from pathlib import Path

import cv2
import numpy as np


def erkenne_farbe(bild):
    """Erkennt die dominante Farbe in einem BGR-Bild."""
    if bild is None or bild.size == 0:
        return "Keine eindeutige Farbe erkannt"

    hsv = cv2.cvtColor(bild, cv2.COLOR_BGR2HSV)

    # Grenzen jeweils als (Farbton, Sättigung, Helligkeit).
    # Die Bereiche überschneiden sich nicht.
    bereiche = {
        "Rot": [
            ((0, 80, 50), (10, 255, 255)),
            ((170, 80, 50), (179, 255, 255)),
        ],
        "Orange": [
            ((11, 80, 50), (19, 255, 255)),
        ],
        "Gelb": [
            ((20, 80, 50), (35, 255, 255)),
        ],
        "Grün": [
            ((36, 80, 50), (84, 255, 255)),
        ],
        "Türkis": [
            ((85, 80, 50), (99, 255, 255)),
        ],
        "Blau": [
            ((100, 80, 50), (130, 255, 255)),
        ],
        "Lila": [
            ((131, 80, 50), (154, 255, 255)),
        ],
        "Pink": [
            ((155, 80, 50), (169, 255, 255)),
        ],
        "Schwarz": [
            ((0, 0, 0), (179, 255, 49)),
        ],
        "Weiß": [
            ((0, 0, 200), (179, 39, 255)),
        ],
        "Grau": [
            ((0, 0, 50), (179, 39, 199)),
            ((0, 40, 50), (179, 79, 255)),
        ],
    }

    anzahl = {}

    for farbe, grenzen in bereiche.items():
        maske = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for unten, oben in grenzen:
            teilmaske = cv2.inRange(
                hsv,
                np.array(unten, dtype=np.uint8),
                np.array(oben, dtype=np.uint8),
            )
            maske = cv2.bitwise_or(maske, teilmaske)

        anzahl[farbe] = cv2.countNonZero(maske)

    rangliste = sorted(anzahl, key=anzahl.get, reverse=True)
    erste, zweite = rangliste[:2]
    gesamtpixel = bild.shape[0] * bild.shape[1]

    # Mindestens 15 % des Bildes müssen zur Farbe passen.
    if anzahl[erste] < gesamtpixel * 0.15:
        return "Keine eindeutige Farbe erkannt"

    # Die stärkste Farbe muss mindestens 1,5-mal so häufig sein
    # wie die zweitstärkste Farbe.
    if anzahl[erste] < anzahl[zweite] * 1.5:
        return "Keine eindeutige Farbe erkannt"

    return erste


if __name__ == "__main__":
    # Das Bild wird im gleichen Ordner wie diese Python-Datei gesucht.
    bildpfad = Path(__file__).resolve().parent / "testbild.jpg"

    bild = cv2.imread(str(bildpfad))

    if bild is None:
        print(f"Bild konnte nicht geladen werden: {bildpfad}")
    else:
        print(f"Ergebnis: {erkenne_farbe(bild)}")