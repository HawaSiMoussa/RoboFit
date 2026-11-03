from pathlib import Path

import cv2
import numpy as np


# HSV-Grenzen: (Farbton, Sättigung, Helligkeit).
# Die Bereiche überschneiden sich nicht.
FARBBEREICHE = {
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


def erkenne_farbe(
    bild,
    mindestanteil=0.15,
    dominanzfaktor=1.5,
    debug=False,
):
    """Gibt die dominante Farbe eines BGR-Bildes zurück.

    Erwartet ein nicht leeres NumPy-Array mit drei Farbkanälen
    und dem Datentyp uint8, beispielsweise von cv2.imread().

    Bei einem ungültigen Eingabebild wird ValueError ausgelöst.
    """
    if (
        not isinstance(bild, np.ndarray)
        or bild.size == 0
        or bild.ndim != 3
        or bild.shape[2] != 3
        or bild.dtype != np.uint8
    ):
        raise ValueError(
            "Erwartet wird ein nicht leeres BGR-Bild "
            "mit drei Kanälen und dem Datentyp uint8."
        )

    if not 0 < mindestanteil <= 1:
        raise ValueError("mindestanteil muss größer als 0 und höchstens 1 sein.")

    if not np.isfinite(dominanzfaktor) or dominanzfaktor <= 1:
        raise ValueError("dominanzfaktor muss endlich und größer als 1 sein.")

    hsv = cv2.cvtColor(bild, cv2.COLOR_BGR2HSV)
    gesamtpixel = bild.shape[0] * bild.shape[1]
    anzahl = {}

    for farbe, grenzen in FARBBEREICHE.items():
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

    if debug:
        print("Farbanteile im gesamten Bild:")

        for farbe in rangliste:
            anteil = anzahl[farbe] / gesamtpixel
            print(f"  {farbe}: {anteil:.1%}")

    if anzahl[erste] < gesamtpixel * mindestanteil:
        return "Keine eindeutige Farbe erkannt"

    if anzahl[erste] < anzahl[zweite] * dominanzfaktor:
        return "Keine eindeutige Farbe erkannt"

    return erste


if __name__ == "__main__":
    # Dateinamen hier an dein Testbild anpassen.
    bildpfad = Path(__file__).resolve().parent / "testbild.jpg"
    bild = cv2.imread(str(bildpfad))

    if bild is None:
        print(f"Bild konnte nicht geladen werden: {bildpfad}")
    else:
        try:
            farbe = erkenne_farbe(bild, debug=True)
            print(f"\nErgebnis: {farbe}")
        except ValueError as fehler:
            print(f"Fehler: {fehler}")