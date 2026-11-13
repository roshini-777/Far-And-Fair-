import json
from db import get_connection, init_db

SAMPLE_STAYS = [
    {
        "name": "Scholar's Haven Co-Living PG",
        "type": "PG",
        "city": "Bengaluru",
        "address": "14th Main, Koramangala 4th Block, Bengaluru 560034",
        "daily_cost": 650,
        "deposit": 5000,
        "rating": 4.7,
        "reviews_count": 142,
        "max_persons": 2,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 12.9352,
        "lng": 77.6245,
        "images": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
            "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800"
        ],
        "description": "Purpose-built student and intern PG featuring dedicated quiet study pods, high-speed fiber Wi-Fi, homestyle breakfast and dinner, and biometric 24/7 entry.",
        "reviews": [
            {"user": "Ananya R.", "rating": 5, "comment": "Super clean study room and zero hidden charges when my deposit was refunded."},
            {"user": "Karthik M.", "rating": 4.5, "comment": "Great food and 10 mins walk to tech offices."}
        ],
        "attractions": [
            {"name": "Cubbon Park", "distance": "5.2 km", "lat": 12.9763, "lng": 77.5929},
            {"name": "Lalbagh Botanical Garden", "distance": "4.8 km", "lat": 12.9507, "lng": 77.5848},
            {"name": "Forum Nexus Mall", "distance": "1.1 km", "lat": 12.9345, "lng": 77.6113}
        ]
    },
    {
        "name": "Backpackers Nest Social Hostel",
        "type": "Hostel",
        "city": "Bengaluru",
        "address": "22 Church Street, Shanthala Nagar, Ashok Nagar, Bengaluru 560001",
        "daily_cost": 520,
        "deposit": 1000,
        "rating": 4.6,
        "reviews_count": 218,
        "max_persons": 4,
        "food_included": 0,
        "wifi": 1,
        "gym": 0,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 12.9749,
        "lng": 77.6074,
        "images": [
            "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800",
            "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800",
            "https://images.unsplash.com/photo-1520277739336-7bf67edfa768?w=800"
        ],
        "description": "Vibrant backpacker and digital nomad hostel right on Church Street with rooftop cafe, locker beds, and coworking lounge.",
        "reviews": [
            {"user": "Rohan S.", "rating": 4.7, "comment": "Metro station is 2 minutes away. Very low deposit!"},
            {"user": "Meera K.", "rating": 4.5, "comment": "Safe solo travel vibe and fast Wi-Fi."}
        ],
        "attractions": [
            {"name": "MG Road Metro & Boulevard", "distance": "0.3 km", "lat": 12.9756, "lng": 77.6066},
            {"name": "Cubbon Park", "distance": "1.2 km", "lat": 12.9763, "lng": 77.5929},
            {"name": "UB City Skydeck", "distance": "1.5 km", "lat": 12.9716, "lng": 77.5963}
        ]
    },
    {
        "name": "Urban Crest Executive Hotel",
        "type": "Hotel",
        "city": "Bengaluru",
        "address": "100 Feet Road, Indiranagar Stage 2, Bengaluru 560038",
        "daily_cost": 1850,
        "deposit": 2000,
        "rating": 4.8,
        "reviews_count": 310,
        "max_persons": 2,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 0,
        "lat": 12.9784,
        "lng": 77.6408,
        "images": [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800"
        ],
        "description": "Modern boutique business hotel with complimentary buffet breakfast, fitness center, ergonomic work desks, and express laundry.",
        "reviews": [
            {"user": "Vikram D.", "rating": 4.9, "comment": "Ideal for week-long work trips. Breakfast spread is awesome."},
            {"user": "Sneha P.", "rating": 4.7, "comment": "Spotless rooms and instant deposit checkout."}
        ],
        "attractions": [
            {"name": "Ulsoor Lake", "distance": "2.6 km", "lat": 12.9817, "lng": 77.6190},
            {"name": "HAL Heritage Aerospace Museum", "distance": "4.9 km", "lat": 12.9547, "lng": 77.6805},
            {"name": "Indiranagar 100ft Cafe Strip", "distance": "0.2 km", "lat": 12.9789, "lng": 77.6405}
        ]
    },
    {
        "name": "GreenView Women's & Student PG",
        "type": "PG",
        "city": "Bengaluru",
        "address": "HSR Layout Sector 2, Near 27th Main, Bengaluru 560102",
        "daily_cost": 580,
        "deposit": 4500,
        "rating": 4.5,
        "reviews_count": 98,
        "max_persons": 3,
        "food_included": 1,
        "wifi": 1,
        "gym": 0,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 12.9121,
        "lng": 77.6446,
        "images": [
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800",
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"
        ],
        "description": "Peaceful residential PG with 3 nutritious meals daily, washing machines on every floor, CCTV + guard security, and bright study lounge.",
        "reviews": [
            {"user": "Priya N.", "rating": 4.6, "comment": "Feels like home. Very safe neighborhood with parks nearby."},
            {"user": "Divya T.", "rating": 4.4, "comment": "Affordable monthly/daily split for interns."}
        ],
        "attractions": [
            {"name": "Agara Lake Park", "distance": "1.4 km", "lat": 12.9234, "lng": 77.6410},
            {"name": "Madiwala Lake", "distance": "3.5 km", "lat": 12.9056, "lng": 77.6177},
            {"name": "HSR Startup Hub", "distance": "0.8 km", "lat": 12.9141, "lng": 77.6389}
        ]
    },
    {
        "name": "MetroPod Smart Capsule Hostel",
        "type": "Hostel",
        "city": "Mumbai",
        "address": "Linking Road, Bandra West, Mumbai 400050",
        "daily_cost": 790,
        "deposit": 1500,
        "rating": 4.7,
        "reviews_count": 184,
        "max_persons": 1,
        "food_included": 0,
        "wifi": 1,
        "gym": 0,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 19.0607,
        "lng": 72.8362,
        "images": [
            "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800",
            "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800",
            "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800"
        ],
        "description": "Private sound-insulated sleeping pods in the heart of Bandra with individual reading lights, high-speed Wi-Fi, and study desks.",
        "reviews": [
            {"user": "Aarav J.", "rating": 4.8, "comment": "Best solo privacy on a student budget in Mumbai!"},
            {"user": "Neha G.", "rating": 4.6, "comment": "Walking distance to Bandstand and great street food."}
        ],
        "attractions": [
            {"name": "Bandra Bandstand Promenade", "distance": "2.1 km", "lat": 19.0427, "lng": 72.8191},
            {"name": "Bandra-Worli Sea Link Viewpoint", "distance": "2.8 km", "lat": 19.0368, "lng": 72.8172},
            {"name": "Mount Mary Basilica", "distance": "2.4 km", "lat": 19.0465, "lng": 72.8224}
        ]
    },
    {
        "name": "Powai Lakeside Intern PG",
        "type": "PG",
        "city": "Mumbai",
        "address": "Hiranandani Gardens, Powai, Mumbai 400076",
        "daily_cost": 850,
        "deposit": 6000,
        "rating": 4.6,
        "reviews_count": 115,
        "max_persons": 2,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 19.1197,
        "lng": 72.9051,
        "images": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"
        ],
        "description": "Premium twin-sharing PG minutes from IIT Bombay and Powai tech parks, complete with gym access, meals, and lake-breeze terrace.",
        "reviews": [
            {"user": "Siddharth V.", "rating": 4.7, "comment": "Saved me tons on commute to Powai offices."},
            {"user": "Riya M.", "rating": 4.5, "comment": "Clean rooms, reliable Wi-Fi, transparent deposit policy."}
        ],
        "attractions": [
            {"name": "Powai Lake Promenade", "distance": "0.9 km", "lat": 19.1268, "lng": 72.9060},
            {"name": "Sanjay Gandhi National Park", "distance": "6.5 km", "lat": 19.2147, "lng": 72.9106},
            {"name": "Galleria Shopping Arcade", "distance": "0.4 km", "lat": 19.1185, "lng": 72.9073}
        ]
    },
    {
        "name": "Marine Bay Boutique Hotel",
        "type": "Hotel",
        "city": "Mumbai",
        "address": "24 Marine Drive, Churchgate, Mumbai 400020",
        "daily_cost": 2200,
        "deposit": 2500,
        "rating": 4.9,
        "reviews_count": 276,
        "max_persons": 2,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 0,
        "lat": 18.9355,
        "lng": 72.8256,
        "images": [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800"
        ],
        "description": "Heritage-view rooms steps away from Marine Drive promenade with breakfast included, 24/7 concierge, and business lounge.",
        "reviews": [
            {"user": "Kabir B.", "rating": 4.9, "comment": "Unbeatable location right across from the sea."},
            {"user": "Tara S.", "rating": 4.8, "comment": "Worth every rupee for short business stays."}
        ],
        "attractions": [
            {"name": "Marine Drive Queen's Necklace", "distance": "0.1 km", "lat": 18.9432, "lng": 72.8230},
            {"name": "Gateway of India", "distance": "2.3 km", "lat": 18.9220, "lng": 72.8347},
            {"name": "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "distance": "1.6 km", "lat": 18.9269, "lng": 72.8326}
        ]
    },
    {
        "name": "Hauz Khas Heritage Hostel",
        "type": "Hostel",
        "city": "Delhi",
        "address": "Hauz Khas Village, Deer Park Road, New Delhi 110016",
        "daily_cost": 480,
        "deposit": 800,
        "rating": 4.6,
        "reviews_count": 195,
        "max_persons": 4,
        "food_included": 1,
        "wifi": 1,
        "gym": 0,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 28.5535,
        "lng": 77.1942,
        "images": [
            "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800",
            "https://images.unsplash.com/photo-1520277739336-7bf67edfa768?w=800",
            "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"
        ],
        "description": "Overlooking lush Deer Park and ancient ruins, offering free breakfast, high-speed Wi-Fi, study tables, and evening acoustic nights.",
        "reviews": [
            {"user": "Devansh A.", "rating": 4.7, "comment": "Incredible park view and super affordable deposit."},
            {"user": "Isha L.", "rating": 4.5, "comment": "Close to IIT Delhi and Green Park metro."}
        ],
        "attractions": [
            {"name": "Hauz Khas Fort & Lake", "distance": "0.3 km", "lat": 28.5546, "lng": 77.1924},
            {"name": "Qutub Minar", "distance": "4.2 km", "lat": 28.5245, "lng": 77.1855},
            {"name": "Lodhi Garden", "distance": "5.5 km", "lat": 28.5931, "lng": 77.2197}
        ]
    },
    {
        "name": "North Campus Scholars PG",
        "type": "PG",
        "city": "Delhi",
        "address": "Kamla Nagar, Near Delhi University North Campus, Delhi 110007",
        "daily_cost": 450,
        "deposit": 3500,
        "rating": 4.4,
        "reviews_count": 160,
        "max_persons": 3,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 1,
        "lat": 28.6814,
        "lng": 77.2045,
        "images": [
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"
        ],
        "description": "Student-friendly PG with all meals, 24/7 reading room, basement gym, and biometric security right beside DU colleges.",
        "reviews": [
            {"user": "Harsh V.", "rating": 4.5, "comment": "Best value near North Campus. Study room stays open all night."},
            {"user": "Simran K.", "rating": 4.3, "comment": "Food quality is consistent and laundry is hassle-free."}
        ],
        "attractions": [
            {"name": "Kamla Nehru Ridge Forest", "distance": "1.1 km", "lat": 28.6852, "lng": 77.2140},
            {"name": "Red Fort (Lal Qila)", "distance": "4.8 km", "lat": 28.6562, "lng": 77.2410},
            {"name": "Majnu Ka Tilla Tibetan Colony", "distance": "2.9 km", "lat": 28.7006, "lng": 77.2273}
        ]
    },
    {
        "name": "Connaught Central Comfort Hotel",
        "type": "Hotel",
        "city": "Delhi",
        "address": "Barakhamba Road, Connaught Place, New Delhi 110001",
        "daily_cost": 1650,
        "deposit": 1500,
        "rating": 4.7,
        "reviews_count": 230,
        "max_persons": 2,
        "food_included": 1,
        "wifi": 1,
        "gym": 1,
        "laundry": 1,
        "security": 1,
        "study_room": 0,
        "lat": 28.6304,
        "lng": 77.2225,
        "images": [
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800"
        ],
        "description": "Central Delhi hotel with complimentary breakfast, metro connectivity across NCR, gym access, and transparent zero-surprise billing.",
        "reviews": [
            {"user": "Nikhil R.", "rating": 4.8, "comment": "Walking distance to Rajiv Chowk Metro. Smooth check-in."},
            {"user": "Pooja M.", "rating": 4.6, "comment": "Clean, safe, and reasonably priced for CP."}
        ],
        "attractions": [
            {"name": "India Gate", "distance": "2.6 km", "lat": 28.6129, "lng": 77.2295},
            {"name": "Jantar Mantar Observatory", "distance": "0.9 km", "lat": 28.6271, "lng": 77.2166},
            {"name": "Agrasen ki Baoli", "distance": "0.8 km", "lat": 28.6261, "lng": 77.2250}
        ]
    }
]


def seed_database(force=False):
    init_db()
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM stays").fetchone()[0]
    if count > 0 and not force:
        conn.close()
        return

    if force:
        conn.execute("DELETE FROM stays")

    for stay in SAMPLE_STAYS:
        conn.execute('''
            INSERT INTO stays (
                name, type, city, address, daily_cost, deposit, rating, reviews_count,
                max_persons, food_included, wifi, gym, laundry, security, study_room,
                lat, lng, images, description, reviews_json, attractions_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            stay["name"], stay["type"], stay["city"], stay["address"],
            stay["daily_cost"], stay["deposit"], stay["rating"], stay["reviews_count"],
            stay["max_persons"], stay["food_included"], stay["wifi"], stay["gym"],
            stay["laundry"], stay["security"], stay["study_room"],
            stay["lat"], stay["lng"],
            json.dumps(stay["images"]),
            stay["description"],
            json.dumps(stay["reviews"]),
            json.dumps(stay["attractions"])
        ))

    conn.commit()
    conn.close()
    print(f"Seeded {len(SAMPLE_STAYS)} accommodations into stays.db successfully.")


if __name__ == "__main__":
    seed_database(force=True)
