from app import create_app
from extensions import db
from models import Tour

app = create_app()

sample = [
    {
        "title": "Uttarakhand Adventure",
        "subtitle": "Mountains, Trekking & Nature",
        "description": "Explore the majestic Himalayas with trekking, river rafting, and serene landscapes.",
        "days": 6,
        "img": "uttarakhand.jpg",
        "price": 1200
    },
    {
        "title": "Jaipur Heritage Tour",
        "subtitle": "Palaces & Culture",
        "description": "Experience the royal palaces, forts, and cultural richness of Jaipur.",
        "days": 4,
        "img": "jaipur.jpg",
        "price": 900
    },
    {
        "title": "Kerala Backwaters",
        "subtitle": "Houses & Nature",
        "description": "Relax in houseboats, enjoy spice gardens and picturesque beaches in Kerala.",
        "days": 7,
        "img": "kerala.jpg",
        "price": 1400
    },
    {
        "title": "Maharashtra Explorer",
        "subtitle": "Mumbai & Hill Stations",
        "description": "From Mumbai’s bustling streets to hill stations, experience the diversity of Maharashtra.",
        "days": 5,
        "img": "maharashtra.jpg",
        "price": 1000
    },
    {
        "title": "Assam & Kaziranga",
        "subtitle": "Tea Gardens & Wildlife",
        "description": "Witness Assam’s tea gardens, rivers, and wildlife sanctuaries including Kaziranga National Park.",
        "days": 6,
        "img": "assam.jpg",
        "price": 1100
    },
    {
        "title": "Kashmir Splendor",
        "subtitle": "Lakes & Valleys",
        "description": "Experience the pristine beauty of Kashmir with Dal Lake, houseboats, and snow-capped mountains.",
        "days": 8,
        "img": "kashmir.jpg",
        "price": 1500
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for s in sample:
        t = Tour(
            title=s['title'], subtitle=s['subtitle'], description=s['description'],
            days=s['days'], img=s['img'], price=s['price']
        )
        db.session.add(t)
    db.session.commit()
    print("Seeded DB with Indian tours")
