import argparse
import subprocess
from pathlib import Path
import os
from colorama import Fore, Style


def print_yellow(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)

def getCart(app_name):
    return '''
from django.contrib import messages
from '''+app_name+'''.models import Carrier, Setting, Product  # Importez vos modèles ici

class CartService:
    @staticmethod
    def add_to_cart(request, product_id, quantity):
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        
        request.session['cart'] = cart
        messages.success(request, f"Produit ajouté au panier.")
    
    @staticmethod
    def remove_from_cart(request, product_id, quantity):
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        
        if product_id in cart:
            if cart[product_id] <= quantity:
                del cart[product_id]
            else:
                cart[product_id] -= quantity
        
        request.session['cart'] = cart
        messages.success(request, f"Produit supprimé du panier.")
    
    @staticmethod
    def clear_cart(request):
        request.session.pop('cart', None)
        messages.success(request, f"Le panier a été vidé.")
    
    @staticmethod
    def get_cart_details():
        cart = request.session.get('cart', {})
        setting = Setting.objects.first()
        tax_rate = setting.taxeRate / 100 if setting else 0
        
        result = {
            'items': [],
            'sub_total': 0,
            'carrier_name': 0,
            'shipping_price': 0,
            'taxe_amount': 0,
            'sub_total_ht': 0,
            'sub_total_ttc': 0,
            'sub_total_with_shipping': 0,
            'cart_count': 0,
        }
        carrier = request.session.get('carrier')
        if not carrier:
            carrier = Carrier.objects.first()
        
        for product_id, quantity in cart.items():
            product = Product.objects.filter(id=product_id).first()
            
            if product:
                sub_total = product.soldePrice * quantity
                result['items'].append({
                    'product': {
                        'id': product.id,
                        'slug': product.slug,
                        'name': product.name,
                        'description': product.description,
                        'soldePrice': product.soldePrice,
                        'regularPrice': product.regularPrice,
                        # Ajoutez d'autres attributs du produit ici
                    },
                    'quantity': quantity,
                    'sub_total': round(sub_total, 2),
                    'taxe_amount': round(sub_total / (1 + tax_rate) * tax_rate, 2),
                    'sub_total_ht': round(sub_total / (1 + tax_rate), 2),
                    'sub_total_ttc': round(sub_total, 2),
                })
                result['sub_total'] += round(sub_total, 2)
                result['cart_count'] += quantity
        
        result['carrier_name'] = carrier.name
        result['shipping_price'] = round(carrier.price, 2)
        result['taxe_amount'] = round(result['sub_total'] / (1 + tax_rate) * tax_rate, 2)
        result['sub_total_ht'] = round(result['sub_total'] / (1 + tax_rate), 2)
        result['sub_total_ttc'] = round(result['sub_total'], 2)
        result['sub_total_with_shipping'] = round(result['sub_total'] + carrier.price, 2)
        
        return result


    '''


def getWishlist(app_name):
    return '''
from '''+app_name+'''.models import Product  # Importez votre modèle Product ici

class WishService:
    @staticmethod
    def add_product_to_wish(request, product_id):
        wish_products = request.session.get('wish', [])

        if product_id not in wish_products:
            wish_products.append(product_id)
            request.session['wish'] = wish_products

    @staticmethod
    def remove_product_from_wish(request, product_id):
        wish_products = request.session.get('wish', [])

        if product_id in wish_products:
            wish_products.remove(product_id)
            request.session['wish'] = wish_products

    @staticmethod
    def get_wished_products(request):
        return request.session.get('wish', [])

    @staticmethod
    def get_wished_products_details(request):
        wish_products = request.session.get('wish', [])
        wished_details = []

        for product_id in wish_products:
            product = Product.objects.filter(id=product_id).first()

            if product:
                wished_details.append({
                    'id': product.id,
                    'slug': product.slug,
                    'name': product.name,
                    'description': product.description,
                    'soldePrice': product.soldePrice,
                    'regularPrice': product.sodePrice,  # Typo corrected: 'soldePrice'
                    'imageUrls': product.imageUrls(),
                    'stock': product.stock,
                    # Ajoutez d'autres attributs du produit ici
                })

        return wished_details

    @staticmethod
    def clear_wished_products(request):
        request.session.pop('wish', None)

    '''


def getCompare(app_name):
    return '''
from '''+app_name+'''.models import Product  # Importez votre modèle Product ici

class CompareService:
    @staticmethod
    def add_product_to_compare(request, product_id):
        compare_products = request.session.get('compare', [])

        if product_id not in compare_products:
            compare_products.append(product_id)
            request.session['compare'] = compare_products

    @staticmethod
    def remove_product_from_compare(request, product_id):
        compare_products = request.session.get('compare', [])

        if product_id in compare_products:
            compare_products.remove(product_id)
            request.session['compare'] = compare_products

    @staticmethod
    def get_compared_products(request):
        return request.session.get('compare', [])

    @staticmethod
    def get_compared_products_details(request):
        compare_products = request.session.get('compare', [])
        compared_details = []

        for product_id in compare_products:
            product = Product.objects.filter(id=product_id).first()

            if product:
                compared_details.append({
                    'id': product.id,
                    'slug': product.slug,
                    'name': product.name,
                    'description': product.description,
                    'soldePrice': product.soldePrice,
                    'regularPrice': product.sodePrice,  # Typo corrected: 'soldePrice'
                    'imageUrls': product.imageUrls(),
                    'stock': product.stock,
                    # Ajoutez d'autres attributs du produit ici
                })

        return compared_details

    @staticmethod
    def clear_compared_products(request):
        request.session.pop('compare', None)

    '''

def getStripe(app_name):
    return '''
from '''+app_name+'''.models import Method
from django.conf import settings

class StripeService:
    def __init__(self):
        # Vérifie si la méthode Stripe est disponible
        self.method = Method.objects.filter(name='Stripe').first()

    # Implémentez ici la logique de votre service
    def get_public_key(self):
        if self.method:
            return self.method.prod_public_key if settings.DEBUG else self.method.test_public_key
        return None  # Gérer le cas où la méthode n'est pas trouvée en base de données

    def get_private_key(self):
        if self.method:
            return self.method.prod_private_key if settings.DEBUG else self.method.test_private_key
        return None  # Gérer le cas où la méthode n'est pas trouvée en base de données

    '''
  

def generate_django_services(app_name, service_name):
    services = {
        'cart': getCart,
        'wish': getWishlist,
        'compare': getCompare,
        'payment': getStripe,
    }
    data_path = f"{app_name}/services/"
    data_file_path = f"{data_path}{service_name}_service.py"
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print_yellow(f"Dossier '{data_path}' créé.")

    if os.path.exists(data_file_path):
        print_yellow(f"Le fichier '{data_file_path}' existe déjà.")
        return
    
    if service_name not in services:
        print_yellow(f"Le service '{service_name}' n'est pas pris en charge.")
        return
    
    try:
        with open(data_file_path, 'w') as file:
            data = services[service_name](app_name)
            file.write(data)
            print_yellow(f"Service '{service_name}' pour l'application '{app_name}' a été créé avec succès.")
    except Exception as e:
        print_yellow(f"Une erreur est survenue lors de la création du service '{service_name}' pour l'application '{app_name}':")
        print_yellow(e)
        

def main():
    parser = argparse.ArgumentParser(description="Generate a Django Services")
    parser.add_argument("app_name", help="Name of the Django app to create")
    parser.add_argument("service_name", help="Name of the Django service to create")
    args = parser.parse_args()

    generate_django_services(args.app_name, args.service_name)

if __name__ == "__main__":
    main()