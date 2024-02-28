# Utilisez une image de base avec Python
FROM python:3.11.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installez les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste de l'application dans le conteneur
COPY . .

# Exposez le port sur lequel l'application Django s'exécute
EXPOSE 8000

# Définissez l'environnement de développement
ENV DJANGO_SETTINGS_MODULE=accessBase.settings
ENV DJANGO_DEBUG=True

# Commande pour démarrer l'application Django avec un redémarrage automatique
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]