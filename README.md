# SQL Scale Test

Projekt pro testování škálovatelnosti a výkonu SQL databází.

## Požadavky

- Docker & Docker Compose
- Python 3.10+
- Poetry

## Rychlý start

1. **Spuštění databáze:**
   ```bash
   docker-compose up -d
   ```

2. **Nastavení Python prostředí:**
   ```bash
   # Instalace závislostí
   poetry install

   # Aktivace virtuálního prostředí
   poetry shell
   ```

3. **Spuštění testů:**
   ```bash
   poetry run pytest
   ```

## Struktura projektu

- `app/`: Zdrojový kód aplikace pro testování.
- `init/`: Inicializační SQL skripty pro databázi.
- `docker-compose.yaml`: Definice PostgreSQL a pgAdmin služeb.
