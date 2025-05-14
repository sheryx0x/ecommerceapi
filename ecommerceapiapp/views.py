from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAdminUser


@api_view(['GET'])
def get_products(request):
    search_query = request.Get.get('search' , '')
    category_id = request.GET.get('category' , None)
    products = Product.objects.all()
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains = search_query))
    if category_id:
        products = products.filter(category_id = category_id)
    serializer = ProductSerializer(products , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_cart(request):
    cart = request.session.get('cart' , {})
    cart_items = []
    for product_id , item in cart.items():
        product = get_object_or_404(Product , id=product_id)
        cart_items.append({
            "product": ProductSerializer(product).data,  
            "quantity": item['quantity'],  
            "total": float(product.price) * item['quantity']  
        })
        return Response(cart_items)
    
@api_view(['POST'])
def add_to_cart(request):
    product_id = str(request.data.get('product_id'))
    quantity = int(request.data.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {'quantity': quantity}

    request.session['cart'] = cart
    request.session.modified = True

    return Response({"message": "Added to cart"}, status=201)


@api_view(['POST'])
def remove_from_cart(request):
    product_id = str(request.data.get('product_id'))
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        return Response({"message": "removed from cart"} , status=200)
    return Response({"message" : "item not found in cart"} , status = 404)



@api_view(['POST'])
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return Response({"message": "Cart cleared"}, status=200)       



