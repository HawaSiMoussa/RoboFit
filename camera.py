
# Schritte 
#   1. Kamera wird geöffnet
#   2. Einzelne Bilder (Frames) von der Kamera werden geholt 
#   3. Das Live Bild wird in einem Fenster anzeigen
#   4. Fehlermeldung, falls die Kamera nicht geht 

# cv2 ist OpenCV und es wird impotiert 
import cv2

# 1 Kamera wird geöffnet 
def open_camera(camera_index=0):
    camera = cv2.VideoCapture(camera_index)
    # VideoCapture ist das OpenCV Objekt das die Kamera steuert.
        # Wir speichern es in der Variable "camera"

    # isOpened() fragt: "Ist die Kamera wirklich offen?" -> True oder False.
    # "not" dreht das um: Wenn die Kamera NICHT offen ist, ...
    if not camera.isOpened():
        # geben wir eine Fehlermeldung aus
        print("FEHLER: Kamera konnte nicht geöffnet werden.")
        print("Tipp: Kamera Erlaubnis fürr das Terminal prüfen.")
        # und geben None zurück 
        return None

    # Wenn alles gut ist, geben wir das Kamera Objekt zurück
    return camera


# 2. Einzelne Bilder (Frames) von der Kamera werden geholt
# Diese Funktion bekommt die offene Kamera (cap) und gibt EIN Bild zurück 
# Genau diese Funktion benutzt spätere die Farberkennung von David
def get_frame(camera):
    # camera.read() macht ein Foto und gibt zwei Dinge zurück:
    #   success = True/False... also  hat es geklappt?
    #   frame   = das Bild selbst in form von eine Tabelle aus Zahlen ein NumPy-Array
    success, frame = camera.read()

    # Wenn es nicht geklappt hat dann fehlermedlung 
    if not success:
        print("FEHLER: Es kam kein Bild von der Kamera.")
        # geben wir None zurück.
        return None

    # Sonst geben wir das Bild zurück
    # WICHTIG: OpenCV speichert Farben als BGR (Blau, Grün, Rot)
    return frame


# 3. Das Live Bild wird in einem Fenster anzeigen
# process_frame=None heisst ---> Man KANN eine Funktion mitgeben (z.B. die
# Farberkennung)
def show_live(process_frame=None, camera_index=0):
    camera = open_camera(camera_index)

    if camera is None:
        return

    print("Kamera läuft. 'q' = Beenden, 's' = Foto machen.")

    # Zaehler, damit jedes Foto einen neuen Namen bekommt
    bild_nummer = 0

    while True:
        frame = get_frame(camera)

        if frame is None:
            break

        image_to_show = frame

        if process_frame is not None:
            result = process_frame(frame)
            if result is not None:
                image_to_show = result

        cv2.imshow("Kamera (q = Beenden, s = Foto machen)", image_to_show)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        # NEU: Wenn die Taste s gedrueckt wird, speichern wir ein Foto
        if key == ord("s"):
            bild_nummer = bild_nummer + 1
            dateiname = f"foto_{bild_nummer}.png"
            cv2.imwrite(dateiname, frame)
            print(f"Foto gespeichert: {dateiname}")

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_live()
