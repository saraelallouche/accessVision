import threading

import pyttsx3
import torch
import numpy as np
import cv2
from time import time
from supervision import BoxAnnotator, Detections
from ultralytics import YOLO
from supervision.draw.color import ColorPalette, Color

from accessVisionBack.model import Element
from accessVisionBack.yolo.utils import getElement


# command for lunch : python accessVisionBack/yolo/yolov8_segmentation.py
class ObjectDetection:

    def __init__(self, capture_index):
        self.tracking = {}
        self.capture_index = capture_index
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = self.load_model()
        self.frame_width = 0
        self.CLASS_NAMES_DICT = self.model.names
        color = Color(255, 0, 0)
        colors = ColorPalette([color,])

        self.box_annotator = BoxAnnotator(color=colors, thickness=3, text_thickness=3, text_scale=1.5)

    def load_model(self):

        model = YOLO("accessVisionBack/yolo/yolov8m.pt")  # load a pretrained YOLOv8n model
        model.fuse()

        return model

    def predict(self, frame):
        results = self.model.track(source=frame, show=True, tracker="bytetrack.yaml", persist=True)
        return results

    def evaluate_distance(self, tracker_id, name, x1, x2):
        element = Element.objects.filter(name=name)
        if element.exists():
            element = element.first()
            size = element.size.size
            largeur_objet_pixels = x2 - x1
            dist = round(self.calculer_distance_objet_camera(largeur_objet_pixels, size, self.frame_width), 2)
            if tracker_id not in self.tracking:
                print("Object " + name + " is at " + str(dist) + " meters from the camera")
                if 2 > dist > 1:
                    self.tracking[tracker_id] = [dist, True]
                    message = element.alerte.format(dist)
                    print(message)
                    threading.Thread(
                        target=self.speak, args=(message,), daemon=True
                    ).start()
                   # Appel de la fonction pour annoncer vocalement le message
                else:
                    self.tracking[tracker_id] = [dist, False]
            else:
                distance = self.tracking[tracker_id][0]
                if 2 > dist > 1 and self.tracking[tracker_id][1] is False:
                    self.tracking[tracker_id] = [dist, True]
                    message = "ATTENTION {} SUR VOTRE CHEMIN à envion {} meters".format(
                         name, dist)
                    print(message)
                    threading.Thread(
                        target=self.speak, args=(message,), daemon=True
                    ).start()  # Appel de la fonction pour annoncer vocalement le message
                elif self.tracking[tracker_id][1] is False:
                    self.tracking[tracker_id] = [dist, False]
                elif self.tracking[tracker_id][1] is True:
                    self.tracking[tracker_id] = [dist, True]
        print(self.tracking)

    def is_center(self, xyxy, name, screen_width, tracker_id):
        x1, y1, x2, y2 = xyxy
        x = (x1 + x2) / 2  # Coordonnée x du centre de l'objet
        center_threshold = 0.2
        min_x = screen_width / 2 - (screen_width * center_threshold)
        max_x = screen_width / 2 + (screen_width * center_threshold)
        if min_x < x < max_x:
            self.evaluate_distance(tracker_id, name, x1, x2)
            print("Object " + name + " is centered horizontally")

    def speak(self, message):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "french")
        self.engine.setProperty('rate', 80)  # setting up new voice rate
        # Fonction pour convertir le texte en voix
        self.engine.say(message)
        self.engine.runAndWait()


    def calculer_distance_objet_camera(self, largeur_objet_pixels, taille_reelle_objet_metres, distance_focale_pixels):
        # Calcul de la distance entre l'objet et la caméra
        distance = (taille_reelle_objet_metres * distance_focale_pixels) / largeur_objet_pixels
        return distance



    def plot_bboxes(self, results, frame):
        # Setup detections for visualization
        track = results[0].boxes.id
        if track is not None:
            detections = Detections(
                xyxy=results[0].boxes.xyxy.cpu().numpy(),
                confidence=results[0].boxes.conf.cpu().numpy(),
                class_id=results[0].boxes.cls.cpu().numpy().astype(int),
                tracker_id=np.array(results[0].boxes.id.int().cpu().tolist())
            )
        else:
            detections = Detections(
                xyxy=results[0].boxes.xyxy.cpu().numpy(),
                confidence=results[0].boxes.conf.cpu().numpy(),
                class_id=results[0].boxes.cls.cpu().numpy().astype(int),
            )

        # Format custom labels
        self.labels = []
        for xyxy, mask, confidence, class_id, tracker_id in detections:
            self.labels.append(f"id = {tracker_id}, {self.CLASS_NAMES_DICT[class_id]} {confidence:0.2f}")
            self.is_center(xyxy, self.CLASS_NAMES_DICT[class_id], self.screen_width, tracker_id)
        # Annotate and display frame
        frame = self.box_annotator.annotate(scene=frame, detections=detections, labels=self.labels)

        return frame

    def __call__(self):
        video_source = 'http://192.168.1.42:4747/video'
        cap = cv2.VideoCapture(video_source)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width, height)
        while True:
            start_time = time()

            ret, frame = cap.read()

            results = self.predict(frame)
            self.frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.screen_width = frame.shape[1]
            frame = self.plot_bboxes(results, frame)

            end_time = time()
            fps = 1 / np.round(end_time - start_time, 2)

            cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            cv2.imshow('YOLOv8 Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


