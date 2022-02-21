

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product

# Create your views here.

def store(request,category_slug=None):
    categories= None
    product=None
    if  category_slug != None:
        categories=get_object_or_404(Category,slug=category_slug)
        product=Product.objects.filter(category=categories,is_available=True)
        product_count=product.count()
    else:
        product=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(product,2)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=product.count()

    context={
        'products':paged_product,
        'product_count':product_count,

    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product)
    except Exception as e:
        raise e

    context={
        'single_product':product,
        'in_cart':in_cart,
    }
  
    return render(request,'store/product_detail.html',context)


def search(request):
    
    product=None
    if 'keyword' in request.GET:
        keyword= request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=product.count()
        else:
            product_count=0
        
    context={
        'products':product,
        'product_count':product_count,
        
    }

    return render(request,'store/store.html',context)

