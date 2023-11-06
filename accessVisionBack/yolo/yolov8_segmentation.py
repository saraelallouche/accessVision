import torch
import numpy as np
import cv2
from time import time
from supervision import BoxAnnotator, Detections
from ultralytics import YOLO
from supervision.draw.color import ColorPalette, Color

# command for lunch : python accessVisionBack/yolo/yolov8_segmentation.py
class ObjectDetection:

    def __init__(self, capture_index):

        self.capture_index = capture_index

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = self.load_model()
        self.trasking_tab = {}

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

    def is_center(self, xyxy, name, screen_width):
        x1, y1, x2, y2 = xyxy
        x = (x1 + x2) / 2  # Coordonnée x du centre de l'objet
        center_threshold = 0.2
        min_x = screen_width / 2 - (screen_width * center_threshold)
        max_x = screen_width / 2 + (screen_width * center_threshold)
        if min_x < x < max_x:
            print("Object " + name + " is centered horizontally")
            # Exemple d'utilisation
            if name == "chair":
                largeur_objet_pixels = x2 - x1  # Largeur de l'objet dans l'image en pixel
                taille_reelle_objet_metres = 0.47  # Taille réelle de l'objet en mètres
                distance_focale = 4.2  # Distance focale de la caméra en pixels
                dist = self.calculer_distance_objet_camera(largeur_objet_pixels, taille_reelle_objet_metres, distance_focale)
                print("Object " + name + " is at "+ str(dist) + " meters from the camera")

            if name == "bottle":
                largeur_objet_pixels = x2 - x1  # Largeur de l'objet dans l'image en pixel
                taille_reelle_objet_metres = 0.12  # Taille réelle de l'objet en mètres
                distance_focale = 4200  # Distance focale de la caméra en pixels
                dist = self.calculer_distance_objet_camera(largeur_objet_pixels, taille_reelle_objet_metres, distance_focale)
                print("Object " + name + " is at "+ str(dist) + " meters from the camera")

    def calculer_distance_objet_camera(self, largeur_objet_pixels, taille_reelle_objet_metres, distance_focale_pixels):
        # Calcul de la distance entre l'objet et la caméra
        distance = (taille_reelle_objet_metres * distance_focale_pixels) / largeur_objet_pixels
        return distance



    def plot_bboxes(self, results, frame):
        # Setup detections for visualization
        detections = Detections(
            xyxy=results[0].boxes.xyxy.cpu().numpy(),
            confidence=results[0].boxes.conf.cpu().numpy(),
            class_id=results[0].boxes.cls.cpu().numpy().astype(int),
            tracker_id=np.array(results[0].boxes.id.int().cpu().tolist())

        )
        # Format custom labels
        self.labels = []
        for xyxy, mask, confidence, class_id, tracker_id in detections:
            self.labels.append(f"id = {tracker_id}, {self.CLASS_NAMES_DICT[class_id]} {confidence:0.2f}")
            self.is_center(xyxy, self.CLASS_NAMES_DICT[class_id], self.screen_width)
        # Annotate and display frame
        frame = self.box_annotator.annotate(scene=frame, detections=detections, labels=self.labels)

        return frame

    def __call__(self):
        video_source = 'http://10.31.44.199:4747/video'
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            start_time = time()

            ret, frame = cap.read()

            results = self.predict(frame)
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


detector = ObjectDetection(capture_index=0)
detector()