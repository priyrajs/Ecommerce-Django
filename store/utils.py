import json
from . models import *

def cookieCart(requests):
    try:
        cart = json.loads(requests.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    items = []
    order = {'get_cart_items': 0, 'get_cart_total':0 }
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            course = Course.objects.get(id=i)
            print(course)
            total = (course.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'course' : {
                    'id': course.id,
                    'name': course.name,
                    'price': course.price,
                    'imageURL': course.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'getTotal': total,
            }
            print(total)

            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(requests):
    if requests.user.is_authenticated:
        customer = requests.user.customer
        print(customer.mdl_user_id)
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(requests)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}