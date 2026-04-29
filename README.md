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

3. **Generování a import dat:**
   ```bash
   # Generování CSV souborů (users, posts, comments)
   poetry run python generator.py

   # Import do běžícího kontejneru
   docker cp users.csv primary-db:/tmp/users.csv
   docker cp posts.csv primary-db:/tmp/posts.csv
   docker cp comments.csv primary-db:/tmp/comments.csv

   # Spuštění importu (COPY)
   docker exec primary-db psql -U user -d scaling_test -c "COPY users(id, username, created_at) FROM '/tmp/users.csv' WITH (FORMAT CSV, DELIMITER ',');"
   docker exec primary-db psql -U user -d scaling_test -c "COPY posts(id, user_id, title, content, created_at) FROM '/tmp/posts.csv' WITH (FORMAT CSV, DELIMITER ',');"
   docker exec primary-db psql -U user -d scaling_test -c "COPY comments(id, post_id, user_id, comment_text, created_at) FROM '/tmp/comments.csv' WITH (FORMAT CSV, DELIMITER ',');"
   ```

4. **Spuštění testů:**
   ```bash
   poetry run pytest
   ```

## Struktura projektu

- `app/`: Zdrojový kód aplikace pro testování.
- `init/`: Inicializační SQL skripty pro databázi.
- `docker-compose.yaml`: Definice PostgreSQL a pgAdmin služeb.
