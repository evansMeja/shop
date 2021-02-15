from django.shortcuts import *
from .models import *
from django.contrib.auth import *
from django.db.models import *
from django.contrib.auth.models import *
from django.http import *
from .user_modules import *
from django.contrib.auth.decorators import user_passes_test
from superuser.models import Categories, Item, TT
from public.models import cart,order, cartitemdetail
from twilio.rest import Client
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
import json

@user_passes_test(is_user, login_url='/login/')
def orderpdf(request):
    order_list = order.objects.filter(callnumber=request.user.username)
    template_path = 'food_delivery_user/orderpdf.html'
    Context = {'order_list':order_list,}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="myorders.pdf"'
    template = get_template(template_path)
    html = template.render(Context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@user_passes_test(is_user, login_url='/login/')
def order_detail(request):
    order_id = request.POST.get("order")
    inst = order.objects.get(pk=order_id)
    cartitemobj=cartitemdetail.objects.filter(owner=inst)
    template_name='food_delivery_user/order_detail.html'
    context={'cartitemobj':cartitemobj,}
    return render(request,template_name,context)

def orderdetailspdf(request):
    order_id = request.POST.get("order")
    inst = order.objects.get(pk=order_id)
    cartitemobj=cartitemdetail.objects.filter(owner=inst)
    template_name='food_delivery_user/orderdetailpdf.html'
    Context={'cartitemobj':cartitemobj,}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orderdetails.pdf"'
    template = get_template(template_name)
    html = template.render(Context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def index(request):
	order_list = order.objects.filter(callnumber=request.user.username)
	template_name='food_delivery_user/index.html'
	context={'order_list':order_list,}
	return render(request,template_name,context)

def checkout(request):
    encoded_cart_data = request.POST.get('jsoncart')
    context={'encoded_cart_data':encoded_cart_data}
    template_name='food_delivery_user/checkout.html'
    return render(request, template_name,context)

def validate_login(request):
	data={}
	if request.user.is_authenticated:
		data["is_authenticated"]=True
		return JsonResponse(data)
	username=request.POST.get('phone')
	password=request.POST.get('password')
	user=authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		data["is_authenticated"]=True
		return JsonResponse(data)
	data["is_authenticated"]=False
	return JsonResponse(data)

def validate_register(request):
	data={}
	if request.user.is_authenticated:
		data["is_authenticated"]=True
		return JsonResponse(data)
	username=request.POST.get('phone')
	password=request.POST.get('password')
	fname=request.POST.get('fname')
	lname=request.POST.get('lname')
	if User.objects.filter(username=username).exists():
		objuser=User.objects.get(username=username)
		objuser.set_password(password)
		objuser.save()
		user=authenticate(request, username=username, password=password)
		login(request, user)
		data["is_authenticated"]=True
		return JsonResponse(data)
	User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
	user=authenticate(request, username=username, password=password)
	login(request, user)
	data["is_authenticated"]=True
	return JsonResponse(data)
	
def create_order(request):
    data={}
    if request.user.is_authenticated:
        data['user_is_authenticated']=True
        in_data = request.GET.get('data')
        s1 = json.dumps(in_data)
        d2 = json.loads(s1)
        order_obj = order()
        order_dict = json.loads(d2)
        order_obj.counter = order_dict['counter']
        order_obj.subtotal = order_dict['subtotal']
        order_obj.callnumber = request.user.username
        order_obj.is_delivered = False
        order_obj.owner = request.user
        order_obj.save()
        
        
        length = len(order_dict['cartItems']) 
        i = 0
        while i < length:
            cartitemdetail_obj = cartitemdetail()
            cartitemdetail_obj.Name = order_dict['cartItems'][i]['price_obj'][0]['Name']
            cartitemdetail_obj.Price = int(order_dict['cartItems'][i]['price_obj'][0]['Price'])
            cartitemdetail_obj.Quantity = order_dict['cartItems'][i]['price_obj'][0]['Quantity']
            cartitemdetail_obj.Picture = order_dict['cartItems'][i]['price_obj'][0]['Picture']
            
            catpk = int(order_dict['cartItems'][i]['price_obj'][0]['Category'])
            cat_obj = Categories.objects.get(pk=catpk)
            cartitemdetail_obj.Category = cat_obj
            i += 1
            cartitemdetail_obj.owner = order_obj
            cartitemdetail_obj.save()
        data['user_is_authenticated']=True
    else:
        data['user_is_authenticated']=False
    return JsonResponse(data)



def remove(request):
	cartid=request.GET.get('cartid')
	cartobj=cart.objects.get(id=cartid)
	cartobj.delete()
	data={'status':"Success",}
	return JsonResponse(data)

def item_detail(request, itemid):
	if request.session.get('has_cart', False):
		addons=cart.objects.filter(sessionid=request.session['cartid'])
		count = cart.objects.filter(sessionid=request.session['cartid']).count()
		total=cart.objects.filter(sessionid=request.session['cartid']).aggregate(Sum('itemprice'))
		total=total["itemprice__sum"]
	else:
		count=0
		addons={}
		total=0
	category_list=Categories.objects.all()
	itemobj=Item.objects.get(id=itemid)
	context={'itemobj':itemobj,'category_list':category_list,'addons':addons,'count':count,'total':total}
	template_name='food_delivery_user/item_detail.html'
	return render(request, template_name, context)


