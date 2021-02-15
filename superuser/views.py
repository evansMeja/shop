from django.shortcuts import *
from django.http import *
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test
from .admin_modules import *
from public.models import cart, order

def manage_order(request):
	sessionid = request.POST.get('sessionid')
	cart_list = cart.objects.filter(sessionid=sessionid)
	template_name='food_delivery_admin/manage_order.html'
	context={'cart_list':cart_list, 'orderid':sessionid,}
	return render(request,template_name,context)

@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard(request):
	template_name='food_delivery_admin/admin_dashboard.html'
	order_list = order.objects.all()
	context={"order_list":order_list}
	return render(request,template_name,context)

@user_passes_test(is_admin, login_url='/login/')
def newitem(request):
	if request.method == 'POST' and request.FILES['picture']:
		name=request.POST.get('name')
		price=request.POST.get('price')
		category=request.POST.get('category')
		quantity=request.POST.get('quantity')
		shortdesc=request.POST.get('shortdesc')
		longdesc=request.POST.get('longdesc')
		picture = request.FILES['picture']
		fs = FileSystemStorage()
		filename = fs.save(picture.name, picture)
		file_url = fs.url(filename)
		categorypk = Categories.objects.get(Name=category)

		Item_obj = Item()
		Item_obj.Category = categorypk
		Item_obj.Name=name
		Item_obj.Price=price
		Item_obj.Quantity=quantity
		Item_obj.Picture=filename
		Item_obj.ShortDesc=shortdesc
		Item_obj.LongDesc=longdesc
		Item_obj.save()
		return HttpResponseRedirect(reverse("admin_dashboard"))
	template_name='food_delivery_admin/newitems.html'
	category_list=Categories.objects.all()
	context={'category_list':category_list,}
	return render(request,template_name,context)
def status(request):
	orderid=request.GET.get('orderid')
	orderobj=order.objects.get(sessionid=orderid)
	orderobj.is_delivered=True
	orderobj.save()
	data={'status':"Success",}
	return JsonResponse(data)

def updatecallnumber(request):
	data={}
	return JsonResponse(data)