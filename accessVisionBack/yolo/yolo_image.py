import json
import threading

import pyttsx3
from pydub import AudioSegment

from accessVisionBack.model import Element, Tracking


def operation(xyxy, name, id, ip):
    x1, y1, x2, y2 = xyxy
    x = (x1 + x2) / 2  # Coordonnée x du centre de l'objet
    center_threshold = 0.3
    min_x = 0.5 - center_threshold
    max_x = 0.5 + center_threshold
    if min_x < x < max_x:
        return evaluate_distance(name, y1, y2, ip, id)


def save_tracking(name, dist, id, ip):
    from django.utils import timezone
    from datetime import timedelta
    is_new = True
    tracking = Tracking.objects.filter(ip=ip)
    name_track = name + "_" + str(id)
    print(name_track)
    if tracking and timezone.now() - tracking.latest("updated_at").updated_at < timedelta(
            minutes=30
    ):
        print("tracking existe")
        last_tracking = tracking.latest("updated_at")
        new_track = json.loads(last_tracking.tracking.replace("'", "\""))
        print('new_track', new_track)
        if name_track in new_track:
            is_new = False
        else:
            new_track[name_track] = dist
            last_tracking.tracking = new_track
            last_tracking.save()

    else:
        print("tracking n'existe pas")
        new_tracking = Tracking.objects.create(
            ip=ip, tracking={name_track: dist}
        )
    return is_new


def evaluate_distance(name, y1, y2, ip, id):
    element = Element.objects.filter(name=name.lower())
    if element.exists():
        element = element.first()
        size = element.size.size
        largeur_objet_pixels = y2 - y1
        print(largeur_objet_pixels.item())
        dist = round((size * 1.1) / float(largeur_objet_pixels.item()), 2)
        name = element.name
        print("Object " + name + " is at " + str(dist) + " meters from the camera")
        if 2 > dist > 0:
            # vérifie si l'élémnt à déjà été détécté
            is_new = save_tracking(name, dist, id, ip)
            print(is_new)
            if is_new:
                message = element.alerte
                print(message)
                audio = speak(message)
                return audio

    else:
        print("object trop éloigné")


def speak(message):
    engine = pyttsx3.init()
    engine.setProperty('voice', "french")
    engine.setProperty('rate', 80)  # setting up new voice rate
    # Fonction pour convertir le texte en voix
    engine.say(message)
    engine.save_to_file(message, 'static/mp3/test2.wav')
    engine.runAndWait()
    return 'static/mp3/test2.wav'
