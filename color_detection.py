import cv2
import numpy as np


def erkenne_farbe(bild):
    """Erwartet ein BGR-Bild, z. B. von cv2.imread()."""
    if bild is None or bild.size == 0:
        return "Keine eindeutige Farbe erkannt"

    hsv = cv2.cvtColor(bild, cv2.COLOR_BGR2HSV)

    # Grenzen jeweils als (H, S, V).
    # Rot liegt an beiden Enden der Farbtonskala.
    bereiche = {
        "Rot": [
            ((0, 80, 50), (10, 255, 255)),
            ((170, 80, 50), (179, 255, 255)),
        ],
        "Gelb": [
            ((20, 80, 50), (35, 255, 255)),
        ],
        "Blau": [
            ((100, 80, 50), (130, 255, 255)),
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

    # Die stärkste Farbe muss deutlich häufiger sein als die zweite.
    if anzahl[erste] < anzahl[zweite] * 1.5:
        return "Keine eindeutige Farbe erkannt"

    return erste


# Wird nur ausgeführt, wenn diese Datei direkt gestartet wird.
if __name__ == "__main__":
    bild = cv2.imread("testbild.jpg")
    print(erkenne_farbe(bild))