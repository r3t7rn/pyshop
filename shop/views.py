from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from shop.models import Product
from cart.models import Item
from cart.cart import Cart

# Create your views here.
def index(request):
    products = Product.objects.all()    #使用ORM执行SELECT * FROM shop_products 查询所有商品，传入模板
    return render(request, 'index.html',locals())

def login(request):
    return render(request, 'Login.html')

def showProduct(request):
    product_id = request.GET.get('id')
    product = get_object_or_404(Product,pk=product_id)   #使用ORM执行SELECT * FROM shop_products where id = pk 查询所有商品,并传入模板 若查询失败，则返回404页面
    print(product)
    return render(request, 'showProduct.html',locals())

def cart(request):
    product = Product.objects.all()   #使用ORM执行SELECT * FROM shop_products 查询所有商品，传入模板
    cart = Cart(request)              #使用ORM执行SELECT * FROM cart_item 查询购物车中所有商品，传入模板
    print(cart,request.session['CART-ID'])
    return render(request, 'cart.html',locals())

def add_to_cart(request):
    product_id = request.POST.get('id')
    quantity = request.POST.get('quantity')
    print(product_id,quantity)
    product = Product.objects.get(id=product_id)  #使用ORM执行SELECT * FROM shop_products where id = product_id 查询商品
    cart = Cart(request)
    incart = Item.objects.filter(cart=cart.cart, object_id=product_id)  #使用ORM执行SELECT * FROM cart_item where object_id = product_id 查询购物车中商品
    print(quantity, product.stock)
    if incart.exists():  #看购物车中是否有此商品
        if incart[0].quantity+int(quantity) <= product.stock: #若有，比较购物车内此商品数量加新增数量与库存
            cart.add(product, product.price, quantity)
            return redirect('/cart')
        else:
            message = "库存不足，无法加入购物车"
            return render(request, 'showProduct.html', locals())
    else:
        if int(quantity) <= product.stock: #若无，则比较新增数量与库存
            cart.add(product, product.price, quantity)
            return redirect('/cart')
        else:
            message = "库存不足，无法加入购物车"
            return render(request, 'showProduct.html', locals())

def remove_from_cart(request):
    product_id = request.GET.get('id')
    print(product_id)
    product = Product.objects.get(id=product_id) #使用ORM执行SELECT * FROM shop_products where id = product_id 查询商品
    cart = Cart(request)
    cart.remove(product)
    return redirect('/cart/')

def checkout(request):
    sum = Cart(request).summary()
    cart = Cart(request)
    for item in cart:
        check=Product.objects.get(id=item.object_id) #使用ORM执行SELECT * FROM shop_products where id = item.object_id 查询出购物车内对应的商品
        check.stock-=item.quantity   #使用ORM执行UPDATE shop_product set stock=stock-item.quantity where id = item.object_id 使结算后对应商品的酷讯减少
        check.save()
    cart.clear()
    message = "总花费￥{},购物车已清空".format(sum)
    return render(request, 'cart.html',locals())