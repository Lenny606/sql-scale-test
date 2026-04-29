import csv
from faker import Faker
import random

fake = Faker()
num_users = 10000
num_posts = 50000
num_comments = 1000000 # Změň na 10M pro opravdový test

# Generujeme uživatele
print("Generuji users.csv...")
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, num_users + 1):
        writer.writerow([i, fake.user_name(), fake.date_this_decade()])

# Generujeme příspěvky
print("Generuji posts.csv...")
with open('posts.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, num_posts + 1):
        writer.writerow([
            i, 
            random.randint(1, num_users), # Náhodné ID uživatele
            fake.sentence(),              # Titulek
            fake.text(),                  # Obsah
            fake.date_this_decade()       # Čas
        ])

# Generujeme komentáře
print("Generuji comments.csv...")
with open('comments.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, num_comments + 1):
        writer.writerow([
            i, 
            random.randint(1, num_posts), # Náhodné ID příspěvku
            random.randint(1, num_users), # Náhodné ID uživatele
            fake.sentence(),              # Text komentáře
            fake.date_this_month()        # Čas
        ])

print("CSV soubory vygenerovány!")