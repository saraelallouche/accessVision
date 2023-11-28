from accessVisionBack.model import Element


def is_center(xyxy, name):
    x1, y1, x2, y2 = xyxy
    x = (x1 + x2) / 2  # Coordonnée x du centre de l'objet
    center_threshold = 0.3
    min_x = 0.5 - center_threshold
    max_x = 0.5 + center_threshold
    if min_x < x < max_x:
        evaluate_distance(name, y1, y2)


def evaluate_distance(name, y1, y2):
    element = Element.objects.filter(name=name)
    if element.exists():
        element = element.first()
        size = element.size.size
        largeur_objet_pixels = y2 - y1
        print(largeur_objet_pixels.item())
        dist = round((size * 1.1) / float(largeur_objet_pixels.item()), 2)
        name = element.name
        print("Object " + name + " is at " + str(dist) + " meters from the camera")
        if 2 > dist > 1:
            message = element.alerte.format(dist)
            print(message)


            # Appel de la fonction pour annoncer vocalement le message
        else:
            print("object trop éloigné")



