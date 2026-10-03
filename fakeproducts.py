import mysql.connector
import random

# -----------------------------------
# 1. Connect to MySQL
# -----------------------------------

connection = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="ghanisht",
    database="shoplytics"
)

cursor = connection.cursor()

# -----------------------------------
# 2. Product data by category
# -----------------------------------

products_by_category = {

    1: [  # Electronics
        "Wireless Headphones",
        "Bluetooth Speaker",
        "Smart Watch",
        "Wireless Mouse",
        "Mechanical Keyboard",
        "USB-C Cable",
        "Power Bank",
        "Laptop Stand",
        "Webcam",
        "Gaming Mouse",
        "Bluetooth Earbuds",
        "Portable SSD",
        "Laptop Backpack",
        "Smartphone",
        "Tablet",
        "Computer Monitor",
        "USB Hub"
    ],

    2: [  # Clothing
        "Cotton T-Shirt",
        "Denim Jeans",
        "Hoodie",
        "Casual Shirt",
        "Track Pants",
        "Sports Jacket",
        "Kurta",
        "Sweatshirt",
        "Formal Trousers",
        "Running Shorts",
        "Polo Shirt",
        "Winter Jacket",
        "Cargo Pants",
        "Ethnic Dress",
        "Denim Jacket",
        "Cotton Shorts",
        "Formal Shirt"
    ],

    3: [  # Home & Kitchen
        "Electric Kettle",
        "Coffee Maker",
        "Mixer Grinder",
        "Non-Stick Pan",
        "Dinner Set",
        "Water Bottle",
        "Storage Container",
        "Table Lamp",
        "Bedsheet",
        "Wall Clock",
        "Air Fryer",
        "Cookware Set",
        "Electric Iron",
        "Dining Table Mat",
        "Kitchen Organizer",
        "Vacuum Cleaner",
        "Food Processor"
    ],

    4: [  # Beauty
        "Face Wash",
        "Moisturizer",
        "Shampoo",
        "Conditioner",
        "Sunscreen",
        "Face Serum",
        "Lip Balm",
        "Body Lotion",
        "Perfume",
        "Hair Oil",
        "Face Mask",
        "Body Wash",
        "Hair Conditioner",
        "Makeup Kit",
        "Lipstick",
        "Eye Liner",
        "Hand Cream"
    ],

    5: [  # Sports
        "Cricket Bat",
        "Football",
        "Badminton Racket",
        "Yoga Mat",
        "Dumbbells",
        "Skipping Rope",
        "Tennis Ball",
        "Gym Gloves",
        "Sports Shoes",
        "Cycling Helmet",
        "Basketball",
        "Tennis Racket",
        "Resistance Bands",
        "Cricket Ball",
        "Sports Bag",
        "Running Shoes",
        "Gym Bottle"
    ],

    6: [  # Books
        "Python Programming",
        "Data Science Basics",
        "Machine Learning Guide",
        "SQL for Beginners",
        "Web Development",
        "Artificial Intelligence",
        "Business Analytics",
        "Computer Networks",
        "Operating Systems",
        "Database Management",
        "Deep Learning",
        "Statistics for Data Science",
        "Cyber Security",
        "Computer Architecture",
        "Software Engineering",
        "Cloud Computing",
        "Natural Language Processing"
    ]
}

# -----------------------------------
# 3. Price ranges for each category
# -----------------------------------

price_ranges = {
    1: (1000, 80000),   # Electronics
    2: (400, 5000),     # Clothing
    3: (300, 15000),    # Home & Kitchen
    4: (200, 5000),     # Beauty
    5: (300, 10000),    # Sports
    6: (200, 3000)      # Books
}

# -----------------------------------
# 4. Generate products
# -----------------------------------

products = []

product_id = 1

for category_id, product_list in products_by_category.items():

    for product_name in product_list:

        # Generate selling price
        min_price, max_price = price_ranges[category_id]

        price = round(
            random.uniform(min_price, max_price),
            2
        )

        # Cost is between 55% and 80% of selling price
        cost = round(
            price * random.uniform(0.55, 0.80),
            2
        )

        # Random stock
        stock = random.randint(10, 500)

        products.append(
            (
                product_id,
                product_name,
                category_id,
                price,
                cost,
                stock
            )
        )

        product_id += 1


# -----------------------------------
# 5. Insert products into MySQL
# -----------------------------------

query = """
INSERT IGNORE INTO products
(product_id, product_name, category_id, price, cost, stock)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query, products)

connection.commit()

print(f"{cursor.rowcount} new products inserted.")

# -----------------------------------
# 6. Close connection
# -----------------------------------

cursor.close()
connection.close()

print("Product generation completed!")