from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        Cart.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic gadgets and devices including smartphones, laptops, tablets, and accessories'
            },
            {
                'name': 'Fashion',
                'description': 'Trending fashion items for men, women, and children including clothing, shoes, and accessories'
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Essential home and kitchen appliances, furniture, and decor items'
            },
            {
                'name': 'Books',
                'description': 'Wide collection of books across various genres including fiction, non-fiction, and educational'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment, outdoor gear, fitness accessories, and athletic wear'
            },
            {
                'name': 'Beauty & Personal Care',
                'description': 'Beauty products, skincare, haircare, and personal grooming items'
            },
            {
                'name': 'Toys & Games',
                'description': 'Fun toys and games for children of all ages'
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, parts, tools, and maintenance products'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[category.name] = category
            self.stdout.write(f'  Created category: {category.name}')

        # Create products
        self.stdout.write('Creating products...')
        
        products_data = [
            # Electronics
            {
                'category': categories['Electronics'],
                'name': 'Samsung Galaxy S23 Ultra 256GB',
                'description': 'Premium flagship smartphone with 200MP camera, 6.8" Dynamic AMOLED display, Snapdragon 8 Gen 2 processor, and S Pen support. Capture stunning photos and enjoy seamless multitasking.',
                'price': Decimal('124999.00'),
                'stock': 45
            },
            {
                'category': categories['Electronics'],
                'name': 'Apple iPhone 15 Pro Max 256GB',
                'description': 'Latest iPhone with A17 Pro chip, titanium design, 48MP main camera with 5x optical zoom, and USB-C. Experience the most powerful iPhone ever.',
                'price': Decimal('159999.00'),
                'stock': 32
            },
            {
                'category': categories['Electronics'],
                'name': 'Dell XPS 15 Laptop - Intel Core i7, 16GB RAM, 512GB SSD',
                'description': 'Premium laptop with 15.6" 4K OLED display, 12th Gen Intel Core i7, NVIDIA RTX 4050 graphics. Perfect for content creators and professionals.',
                'price': Decimal('189999.00'),
                'stock': 18
            },
            {
                'category': categories['Electronics'],
                'name': 'Sony WH-1000XM5 Wireless Headphones',
                'description': 'Industry-leading noise cancellation, exceptional sound quality, 30-hour battery life, and multipoint connection. Perfect for music lovers and travelers.',
                'price': Decimal('34999.00'),
                'stock': 67
            },
            {
                'category': categories['Electronics'],
                'name': 'Apple iPad Air 5th Gen 64GB WiFi',
                'description': '10.9" Liquid Retina display, M1 chip, 12MP camera with Center Stage. Powerful, colorful, and versatile for work and play.',
                'price': Decimal('64999.00'),
                'stock': 28
            },
            {
                'category': categories['Electronics'],
                'name': 'LG 55" 4K OLED Smart TV',
                'description': 'Stunning 4K OLED display with perfect blacks, Dolby Vision IQ, webOS smart platform, and AI ThinQ. Transform your living room into a cinema.',
                'price': Decimal('139999.00'),
                'stock': 12
            },
            {
                'category': categories['Electronics'],
                'name': 'Canon EOS R6 Mark II Mirrorless Camera Body',
                'description': '24.2MP full-frame sensor, 40fps continuous shooting, 6K video recording, advanced autofocus. Professional photography made accessible.',
                'price': Decimal('279999.00'),
                'stock': 8
            },
            {
                'category': categories['Electronics'],
                'name': 'Apple AirPods Pro 2nd Generation',
                'description': 'Active noise cancellation, adaptive transparency, personalized spatial audio with dynamic head tracking, and USB-C charging.',
                'price': Decimal('27999.00'),
                'stock': 89
            },
            {
                'category': categories['Electronics'],
                'name': 'Samsung 1TB T7 Portable SSD',
                'description': 'Ultra-fast external storage with read speeds up to 1050MB/s, durable metal design, password protection, and USB-C connectivity.',
                'price': Decimal('14999.00'),
                'stock': 156
            },
            {
                'category': categories['Electronics'],
                'name': 'Logitech MX Master 3S Wireless Mouse',
                'description': 'Ergonomic wireless mouse with 8K DPI sensor, quiet clicks, USB-C charging, and multi-device connectivity. Perfect for productivity.',
                'price': Decimal('11999.00'),
                'stock': 94
            },

            # Fashion
            {
                'category': categories['Fashion'],
                'name': "Levi's 501 Original Fit Jeans - Men's",
                'description': 'Classic straight fit jeans with button fly, made from premium denim. Timeless style that never goes out of fashion.',
                'price': Decimal('7999.00'),
                'stock': 124
            },
            {
                'category': categories['Fashion'],
                'name': 'Nike Air Max 270 Running Shoes',
                'description': 'Comfortable running shoes with large Air unit, breathable mesh upper, and durable rubber outsole. Style meets performance.',
                'price': Decimal('13999.00'),
                'stock': 78
            },
            {
                'category': categories['Fashion'],
                'name': 'Adidas Originals Trefoil Hoodie',
                'description': 'Classic pullover hoodie with iconic trefoil logo, soft cotton blend, and kangaroo pocket. Casual comfort for everyday wear.',
                'price': Decimal('5999.00'),
                'stock': 203
            },
            {
                'category': categories['Fashion'],
                'name': 'Ray-Ban Aviator Classic Sunglasses',
                'description': 'Iconic teardrop shape with gold frame and green G-15 lenses. 100% UV protection with timeless style.',
                'price': Decimal('16999.00'),
                'stock': 56
            },
            {
                'category': categories['Fashion'],
                'name': "Women's Casual Summer Dress - Floral Print",
                'description': 'Lightweight, breathable cotton dress with beautiful floral pattern, perfect for summer outings and beach vacations.',
                'price': Decimal('3999.00'),
                'stock': 167
            },
            {
                'category': categories['Fashion'],
                'name': 'Leather Crossbody Bag - Women',
                'description': 'Genuine leather handbag with adjustable strap, multiple compartments, and elegant design. Perfect for daily use.',
                'price': Decimal('8999.00'),
                'stock': 43
            },
            {
                'category': categories['Fashion'],
                'name': 'Timex Expedition Watch - Men',
                'description': 'Durable field watch with Indiglo night-light, date display, water-resistant design, and genuine leather strap.',
                'price': Decimal('9999.00'),
                'stock': 67
            },
            {
                'category': categories['Fashion'],
                'name': 'Calvin Klein Cotton Boxer Briefs Pack of 3',
                'description': 'Premium cotton boxer briefs with comfortable elastic waistband and CK logo. Essential basics for everyday comfort.',
                'price': Decimal('2999.00'),
                'stock': 289
            },

            # Home & Kitchen
            {
                'category': categories['Home & Kitchen'],
                'name': 'Ninja Foodi 8-Quart Pressure Cooker',
                'description': '14-in-1 multi-cooker that pressure cooks, air fries, slow cooks, and more. Make delicious meals in minutes.',
                'price': Decimal('24999.00'),
                'stock': 34
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'Dyson V15 Detect Cordless Vacuum',
                'description': 'Powerful cordless vacuum with laser dust detection, LCD screen, and up to 60 minutes runtime. Deep clean your entire home.',
                'price': Decimal('74999.00'),
                'stock': 19
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'Nespresso Vertuo Coffee Maker',
                'description': 'Single-serve coffee maker with Centrifusion technology, makes 5 cup sizes, and comes with milk frother. Barista-quality coffee at home.',
                'price': Decimal('21999.00'),
                'stock': 41
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'KitchenAid 5-Quart Stand Mixer',
                'description': 'Iconic stand mixer with 10 speeds, tilt-head design, and includes whisk, beater, and dough hook. Baking made easy.',
                'price': Decimal('44999.00'),
                'stock': 23
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'Egyptian Cotton Bed Sheet Set - Queen',
                'description': '600 thread count luxury sheets made from 100% Egyptian cotton. Soft, breathable, and durable for ultimate comfort.',
                'price': Decimal('8999.00'),
                'stock': 76
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'Philips Hue Smart LED Bulb Starter Kit',
                'description': '4-pack color smart bulbs with bridge, 16 million colors, voice control compatible, and automation features.',
                'price': Decimal('18999.00'),
                'stock': 52
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'Samsonite 3-Piece Luggage Set',
                'description': 'Hardside spinner luggage set with TSA locks, 360° wheels, and expandable design. Travel with style and convenience.',
                'price': Decimal('32999.00'),
                'stock': 28
            },
            {
                'category': categories['Home & Kitchen'],
                'name': 'InstantPot Duo Plus 6 Quart',
                'description': '9-in-1 electric pressure cooker with sterilize, yogurt maker, slow cooker, and more. Quick, easy, and delicious meals.',
                'price': Decimal('12999.00'),
                'stock': 91
            },

            # Books
            {
                'category': categories['Books'],
                'name': 'Atomic Habits by James Clear',
                'description': 'Transform your life with tiny changes that deliver remarkable results. A proven framework for improving every day.',
                'price': Decimal('1899.00'),
                'stock': 234
            },
            {
                'category': categories['Books'],
                'name': 'The Psychology of Money by Morgan Housel',
                'description': 'Timeless lessons on wealth, greed, and happiness. Learn how to think about money and make better financial decisions.',
                'price': Decimal('1699.00'),
                'stock': 187
            },
            {
                'category': categories['Books'],
                'name': 'Sapiens: A Brief History of Humankind by Yuval Noah Harari',
                'description': 'Explore the history of our species from the Stone Age to the present. A groundbreaking narrative of human evolution.',
                'price': Decimal('1999.00'),
                'stock': 156
            },
            {
                'category': categories['Books'],
                'name': 'The Alchemist by Paulo Coelho',
                'description': 'Follow Santiago on his journey to find treasure and discover his personal legend. An inspiring tale of following your dreams.',
                'price': Decimal('1299.00'),
                'stock': 298
            },
            {
                'category': categories['Books'],
                'name': '48 Laws of Power by Robert Greene',
                'description': 'Distilled wisdom of philosophers, strategists, and warriors. Learn the timeless laws of power and strategy.',
                'price': Decimal('2199.00'),
                'stock': 143
            },
            {
                'category': categories['Books'],
                'name': 'Think and Grow Rich by Napoleon Hill',
                'description': 'The original personal development classic. Discover the secret to success used by Andrew Carnegie and Henry Ford.',
                'price': Decimal('999.00'),
                'stock': 412
            },

            # Sports & Outdoors
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Bowflex SelectTech 552 Adjustable Dumbbells (Pair)',
                'description': 'Space-saving adjustable dumbbells that replace 15 sets of weights. Weight range: 5-52.5 lbs per dumbbell.',
                'price': Decimal('54999.00'),
                'stock': 15
            },
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Yeti Rambler 30oz Tumbler',
                'description': 'Insulated stainless steel tumbler that keeps drinks cold for 24 hours or hot for 6 hours. Durable and dishwasher safe.',
                'price': Decimal('4999.00'),
                'stock': 178
            },
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Manduka PRO Yoga Mat',
                'description': 'Professional-grade yoga mat with superior cushioning, unparalleled grip, and lifetime guarantee. Perfect for all practices.',
                'price': Decimal('11999.00'),
                'stock': 67
            },
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Garmin Forerunner 255 GPS Running Watch',
                'description': 'Advanced running watch with training metrics, recovery insights, race predictions, and up to 14-day battery life.',
                'price': Decimal('44999.00'),
                'stock': 23
            },
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Wilson Evolution Indoor Basketball',
                'description': 'Official size basketball with cushioned core technology and superior grip. The choice of high school and college players.',
                'price': Decimal('6999.00'),
                'stock': 89
            },
            {
                'category': categories['Sports & Outdoors'],
                'name': 'Coleman 6-Person Camping Tent',
                'description': 'Easy-setup tent with WeatherTec system, room divider, and large windows. Perfect for family camping adventures.',
                'price': Decimal('17999.00'),
                'stock': 34
            },

            # Beauty & Personal Care
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'CeraVe Moisturizing Cream 453g',
                'description': 'Dermatologist-developed moisturizer with ceramides and hyaluronic acid. Provides 24-hour hydration for dry skin.',
                'price': Decimal('1899.00'),
                'stock': 267
            },
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'Olaplex Hair Perfector No. 3',
                'description': 'Professional-quality at-home treatment that repairs damaged hair, reduces breakage, and strengthens bonds.',
                'price': Decimal('3499.00'),
                'stock': 145
            },
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'Neutrogena Hydro Boost Water Gel 50ml',
                'description': 'Oil-free facial moisturizer with hyaluronic acid. Provides intense hydration and leaves skin smooth and supple.',
                'price': Decimal('1499.00'),
                'stock': 312
            },
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'Gillette Fusion5 ProGlide Razor + 8 Cartridges',
                'description': 'Advanced razor with FlexBall technology and precision trimmer. Provides a smooth, comfortable shave.',
                'price': Decimal('3999.00'),
                'stock': 198
            },
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'Maybelline Sky High Mascara',
                'description': 'Lengthening mascara with Flex Tower brush for full volume and limitless length. Waterproof formula available.',
                'price': Decimal('1299.00'),
                'stock': 423
            },
            {
                'category': categories['Beauty & Personal Care'],
                'name': 'The Ordinary Niacinamide 10% + Zinc 1% Serum',
                'description': 'High-strength vitamin and mineral blemish formula that reduces the appearance of pores and uneven skin tone.',
                'price': Decimal('999.00'),
                'stock': 534
            },

            # Toys & Games
            {
                'category': categories['Toys & Games'],
                'name': 'LEGO Star Wars Millennium Falcon',
                'description': '7,541-piece ultimate collector series set. Includes minifigures and detailed interior. Perfect for display and play.',
                'price': Decimal('89999.00'),
                'stock': 12
            },
            {
                'category': categories['Toys & Games'],
                'name': 'Nintendo Switch OLED Console',
                'description': 'Gaming console with vibrant 7-inch OLED screen, enhanced audio, and adjustable stand. Play at home or on the go.',
                'price': Decimal('37999.00'),
                'stock': 45
            },
            {
                'category': categories['Toys & Games'],
                'name': 'Barbie Dreamhouse Playset',
                'description': '3-story dollhouse with 8 rooms, pool, slide, elevator, and lights & sounds. Includes 70+ accessories.',
                'price': Decimal('24999.00'),
                'stock': 28
            },
            {
                'category': categories['Toys & Games'],
                'name': 'Hot Wheels Ultimate Garage Playset',
                'description': 'Massive 3+ feet tall garage with parking for 140+ cars, motorized elevator, and menacing shark. Epic play adventure.',
                'price': Decimal('19999.00'),
                'stock': 19
            },
            {
                'category': categories['Toys & Games'],
                'name': 'Monopoly Classic Board Game',
                'description': 'The timeless property trading game for 2-6 players. Buy, sell, and trade properties to become the wealthiest player.',
                'price': Decimal('3999.00'),
                'stock': 167
            },

            # Automotive
            {
                'category': categories['Automotive'],
                'name': 'Garmin DriveSmart 65 GPS Navigator',
                'description': '6.95" touchscreen GPS with voice-activated navigation, live traffic updates, and driver alerts.',
                'price': Decimal('27999.00'),
                'stock': 34
            },
            {
                'category': categories['Automotive'],
                'name': 'Black+Decker Portable Car Vacuum',
                'description': 'Powerful 12V DC vacuum with flexible hose, crevice tool, and brush attachment. Keep your car spotless.',
                'price': Decimal('4999.00'),
                'stock': 123
            },
            {
                'category': categories['Automotive'],
                'name': 'Rain-X Windshield Treatment 207ml',
                'description': 'Advanced water repellent that improves visibility in rain, sleet, and snow. Apply every 3-6 months.',
                'price': Decimal('899.00'),
                'stock': 456
            },
            {
                'category': categories['Automotive'],
                'name': 'Michelin 12V Digital Tire Inflator',
                'description': 'Programmable digital gauge, auto shut-off, LED light, and carries up to 120 PSI. Essential for every car.',
                'price': Decimal('5999.00'),
                'stock': 87
            },
            {
                'category': categories['Automotive'],
                'name': 'ArmorAll Original Protectant 473ml',
                'description': 'Protects and restores dashboard, vinyl, rubber, and plastic surfaces. UV protection prevents fading and cracking.',
                'price': Decimal('1299.00'),
                'stock': 312
            },
        ]

        for product_data in products_data:
            product = Product.objects.create(
                category=product_data['category'],
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                is_active=True
            )
            self.stdout.write(f'  Created product: {product.name}')

        # Create sample users with carts
        self.stdout.write('Creating sample users...')
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
        ]

        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            # Create cart for each user
            Cart.objects.create(user=user)
            self.stdout.write(f'  Created user: {user.username}')

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('  Created superuser: admin (password: admin123)'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {Product.objects.count()} products'))
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.filter(is_superuser=False).count()} regular users'))
        self.stdout.write(self.style.SUCCESS('\nYou can login with:'))
        self.stdout.write('  Admin: username=admin, password=admin123')
        self.stdout.write('  User: username=john_doe, password=password123')