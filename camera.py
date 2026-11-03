
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
    # VideoCapture ist das OpenCV-Objekt, das die Kamera steuert.
        # Wir speichern es in der Variable "cap"

    # isOpened() fragt: "Ist die Kamera wirklich offen?" -> True oder False.
    # "not" dreht das um: Wenn die Kamera NICHT offen ist, ...
    if not cap.isOpened():
        # geben wir eine Fehlermeldung aus
        print("FEHLER: Kamera konnte nicht geoeffnet werden.")
        print("Tipp: Kamera-Erlaubnis fuer das Terminal pruefen oder camera_index=1 probieren.")
        # und geben None zurück 
        return None
