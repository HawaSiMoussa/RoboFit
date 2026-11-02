#OpenCV Bibliothek importieren (zur Video-und Bildverarbeitung)
import cv2 

#zum Öffnen der Laptop Kamera
def open_camera():
    #0 steht für Standardkamera (also die meines Laptops) und wenn da 1 oder 2 kann man auch andere Kameras auswählen
    camera = cv2.VideoCapture(0)
#isOpened() gibt True zurück, wenn alles geklappt hat
    if not camera.isOpened():
        raise RuntimeError("Kamera konnte nicht geöffnet werden.")

    return camera
