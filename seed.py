from app import create_app
from extensions import db
from models import Tour

app = create_app()

# Sample tours without hotels, ready for gallery and cuisine images
sample = [
    {
        "title": "Uttarakhand Adventure",
        "subtitle": "Mountains, Trekking & Nature",
        "description": "Explore the majestic Himalayas with trekking, river rafting, and serene landscapes.",
        "days": 6,
        "img": "uttarakhand.jpg",
        "price": 1200,
        "highlights": ["Himalayan trekking", "River rafting", "Camping under stars"],
        "places_to_visit": ["Rishikesh", "Mussoorie", "Nainital", "Valley of Flowers"],
        "cuisine": ["Aloo Ke Gutke", "Bhatt ki Churdkani", "Bal Mithai"],
        "history": "Uttarakhand, known as Devbhoomi, is famed for its temples, trekking routes, and natural beauty.",
        "gallery": ["uttarakhand1.jpg", "uttarakhand2.jpg", "uttarakhand3.jpg"],
        "welcome_msg": "स्वागत है उत्तराखंड एडवेंचर में!"
    },
    {
        "title": "Jaipur Heritage Tour",
        "subtitle": "Palaces & Culture",
        "description": "Experience the royal palaces, forts, and cultural richness of Jaipur. Explore colorful markets and local crafts.",
        "days": 4,
        "img": "jaipur.jpg",
        "price": 900,
        "highlights": ["Amber Fort", "City Palace", "Local bazaars", "Elephant ride experience"],
        "places_to_visit": ["Amber Fort", "Hawa Mahal", "Jantar Mantar"],
        "cuisine": ["Dal Baati Churma", "Ghewar", "Pyaz Kachori"],
        "history": "Jaipur, the Pink City, is famous for its architecture and forts.",
        "gallery": ["jaipur1.jpg", "jaipur2.jpg", "jaipur3.jpg"],
        "welcome_msg": "जयपुर में आपकौ राम राम!"
    },
    {
        "title": "Kerala Backwaters",
        "subtitle": "Houses & Nature",
        "description": "Relax in houseboats, enjoy spice gardens and picturesque beaches in Kerala.",
        "days": 7,
        "img": "kerala.jpg",
        "price": 1400,
        "highlights": ["Houseboat cruise", "Spice plantations", "Beaches"],
        "places_to_visit": ["Alleppey", "Kumarakom", "Fort Kochi"],
        "cuisine": ["Appam & Stew", "Puttu & Kadala Curry", "Kerala Sadya"],
        "history": "Kerala is known for its lush backwaters, spices, and centuries-old maritime trade.",
        "gallery": ["kerala1.jpg", "kerala2.jpg", "kerala3.jpg"],
        "welcome_msg": "കേരളത്തിലേക്ക് സ്വാഗതം!"
    },
    {
        "title": "Maharashtra Explorer",
        "subtitle": "Mumbai & Hill Stations",
        "description": "From Mumbai’s bustling streets to hill stations, experience the diversity of Maharashtra.",
        "days": 5,
        "img": "maharashtra.jpg",
        "price": 1000,
        "highlights": ["Mumbai city tour", "Hill station trek", "Local cuisine tasting"],
        "places_to_visit": ["Mumbai", "Lonavala", "Pune", "Mahabaleshwar"],
        "cuisine": ["Vada Pav", "Misal Pav", "Puran Poli", "Bombil Fry"],
        "history": "Maharashtra offers a mix of colonial history, Maratha heritage, and scenic hill stations.",
        "gallery": ["maharashtra1.jpg", "maharashtra2.jpg", "maharashtra3.jpg"],
        "welcome_msg": "महाराष्ट्र एक्सप्लोरर मध्ये आपले स्वागत आहे!"
    },
    {
        "title": "Assam & Kaziranga",
        "subtitle": "Tea Gardens & Wildlife",
        "description": "Witness Assam’s tea gardens, rivers, and wildlife sanctuaries including Kaziranga National Park.",
        "days": 6,
        "img": "assam.jpg",
        "price": 1100,
        "highlights": ["Tea garden visit", "Kaziranga Safari", "River cruise"],
        "places_to_visit": ["Kaziranga National Park", "Guwahati", "Majuli Island", "Sivasagar"],
        "cuisine": ["Assamese Thali", "Khaar", "Masor Tenga", "Pitha"],
        "history": "Assam is known for its rich culture, tea gardens, and biodiversity hotspots like Kaziranga.",
        "gallery": ["assam1.jpg", "assam2.jpg", "assam3.jpg"],
        "welcome_msg": "অসমলৈ স্বাগতম!"
    },
    {
        "title": "Kashmir Splendor",
        "subtitle": "Lakes & Valleys",
        "description": "Experience the pristine beauty of Kashmir with Dal Lake, houseboats, and snow-capped mountains.",
        "days": 8,
        "img": "kashmir.jpg",
        "price": 1500,
        "highlights": ["Dal Lake boating", "Houseboat stay", "Gulmarg snow trek"],
        "places_to_visit": ["Srinagar", "Gulmarg", "Pahalgam", "Sonamarg"],
        "cuisine": ["Rogan Josh", "Kahwa Tea", "Gushtaba", "Kashmiri Pulao"],
        "history": "Kashmir, the Paradise on Earth, is famous for its scenic beauty, Mughal gardens, and rich cultural heritage.",
        "gallery": ["kashmir1.jpg", "kashmir2.jpg", "kashmir3.jpg"],
        "welcome_msg": "کشمیری حسن میں خوش آمدید!"
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for s in sample:
        t = Tour(
            title=s['title'],
            subtitle=s['subtitle'],
            description=s['description'],
            days=s['days'],
            img=s['img'],
            price=s['price'],
            highlights=s.get('highlights', []),
            places_to_visit=s.get('places_to_visit', []),
            cuisine=s.get('cuisine', []),
            history=s.get('history', ""),
            gallery=s.get('gallery', []),
            welcome_msg=s.get('welcome_msg', f"Welcome to {s['title']}!")
        )
        db.session.add(t)

    db.session.commit()
    print("Seeded DB with tours, places & cuisine images, hotels removed.")
