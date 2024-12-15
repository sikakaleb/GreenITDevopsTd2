FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le script Python de l'exporter
COPY exporter.py .

# Lancer l'exporter
CMD ["python", "exporter.py"]
