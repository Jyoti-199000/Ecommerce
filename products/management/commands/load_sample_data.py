from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage

class Command(BaseCommand):
    help = 'Load sample products for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        categories_data = [
            {'name': 'Electronics', 'image': 'https://images.unsplash.com/photo-1498049794561-7780e7231661'},
            {'name': 'Fashion', 'image': 'https://images.unsplash.com/photo-1445205170230-053b83016050'},
            {'name': 'Home & Living', 'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571'},
            {'name': 'Books', 'image': 'https://images.unsplash.com/photo-1512820790803-83ca734da794'},
            {'name': 'Sports', 'image': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211'},
            {'name': 'Beauty', 'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'image': cat_data['image']}
            )
            categories[cat.name] = cat
            if created:
                self.stdout.write(f'Created category: {cat.name}')
        
        products_data = [
            {
                'name': 'Wireless Noise-Canceling Headphones',
                'description': 'Premium wireless headphones with active noise cancellation.',
                'category': 'Electronics',
                'price': 149.99,
                'original_price': 249.99,
                'stock': 45,
                'featured': True,
                'rating': 4.5,
                'review_count': 324,
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e'
            },
            {
                'name': 'Smart Watch Pro',
                'description': 'Advanced fitness tracker with heart rate monitoring.',
                'category': 'Electronics',
                'price': 299.99,
                'original_price': 399.99,
                'stock': 30,
                'featured': True,
                'rating': 4.7,
                'review_count': 567,
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30'
            },
            {
                'name': 'Leather Messenger Bag',
                'description': 'Handcrafted genuine leather messenger bag.',
                'category': 'Fashion',
                'price': 89.99,
                'original_price': 129.99,
                'stock': 25,
                'featured': True,
                'rating': 4.3,
                'review_count': 189,
                'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62'
            },
        ]
        
        for prod_data in products_data:
            category = categories[prod_data['category']]
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'category': category,
                    'price': prod_data['price'],
                    'original_price': prod_data['original_price'],
                    'stock': prod_data['stock'],
                    'featured': prod_data['featured'],
                    'is_active': True,
                    'rating': prod_data['rating'],
                    'review_count': prod_data['review_count'],
                }
            )
            
            if created:
                ProductImage.objects.create(
                    product=product,
                    image_url=prod_data['image'],
                    is_primary=True,
                    order=1
                )
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
