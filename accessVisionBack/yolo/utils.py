from accessVisionBack.model import Element


def getElement(name):
    element = Element.objects.filter(name=name)
    if element.exists():
        return element.first()
    return None