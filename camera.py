
# Schritte 
#   1. Kamera wird geöffnet
#   2. Einzelne Bilder (Frames) von der Kamera werden geholt 
#   3. Das Live Bild wird in einem Fenster anzeigen
#   4. Fehlermeldung, falls die Kamera nicht geht 


# cv2 ist OpenCV und es wird impotiert 
import cv2

# 1 Kamera wird geöffnet 
def open_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    # VideoCapture ist das OpenCV Objekt das die Kamera steuert.
        # Wir speichern es in der Variable "cap"

    # isOpened() fragt: "Ist die Kamera wirklich offen?" -> True oder False.
    # "not" dreht das um: Wenn die Kamera NICHT offen ist, ...
    if not cap.isOpened():
        # geben wir eine Fehlermeldung aus
        print("FEHLER: Kamera konnte nicht geöffnet werden.")
        print("Tipp: Kamera Erlaubnis fürr das Terminal prüfen.")
        # und geben None zurück 
        return None

    # Wenn alles gut ist, geben wir das Kamera Objekt zurück
    return cap


# 2. Einzelne Bilder (Frames) von der Kamera werden geholt
# Diese Funktion bekommt die offene Kamera (cap) und gibt EIN Bild zurück 
# Genau diese Funktion benutzt spätere die Farberkennung von David
def get_frame(cap):
    # cap.read() macht ein Foto und gibt zwei Dinge zurück:
    #   success = True/False... also  hat es geklappt?
    #   frame   = das Bild selbst in form von eine Tabelle aus Zahlen ein NumPy-Array
    success, frame = cap.read()

    # Wenn es nicht geklappt hat dann fehlermedlung 
    if not success:
        print("FEHLER: Es kam kein Bild von der Kamera.")
        # geben wir None zurück.
        return None

    # Sonst geben wir das Bild zurück
    # WICHTIG: OpenCV speichert Farben als BGR (Blau, Grün, Rot)
    return frame


