# Utiliser une image de base python 3.9
FROM python:3.9

# Mettre à jour les paquets
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    git

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m myuser
USER myuser

# Définir le répertoire de travail
WORKDIR /home/myuser/app

# Copier les fichiers de l'application dans le conteneur
COPY app app
COPY requirements.txt requirements.txt

# Modifier les permissions du répertoire "app"
RUN sudo chown -R myuser:myuser app

# Installer les dépendances de l'application
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exposer le port 8000 pour permettre l'accès à l'API
EXPOSE 8000

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
