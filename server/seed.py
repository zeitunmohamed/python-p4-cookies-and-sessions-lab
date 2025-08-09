#!/usr/bin/env python3

from random import randint
from faker import Faker

from app import app
from models import db, Article, User

fake = Faker()

with app.app_context():
    print("Clearing and creating database...")
    db.drop_all()
    db.create_all()

    print("Creating users...")
    users = [User(name=fake.name()) for _ in range(25)]
    db.session.add_all(users)
    db.session.commit()  # Commit so users have IDs

    print("Creating articles...")
    articles = []
    for _ in range(100):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + '...'

        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
            user_id=fake.random_element(elements=[u.id for u in users])
        )
        articles.append(article)

    db.session.add_all(articles)
    db.session.commit()

    print("✅ Seeding complete!")
