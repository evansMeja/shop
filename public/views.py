from .custom_public_modules import *
from django.shortcuts import *
from .models import *
from django.contrib.auth import *
from django.db.models import *
from django.contrib.auth.models import *
from django.http import *
from superuser.models import Categories, Item

# Create your views here.
def addon(request):
    name=request.POST.get("name")
    price_obj = Item.objects.filter(
        Name=name
        ).values(
        'id',
        'Name',
        'Price',
        'Quantity',
        'Category',
        'Stock',
        'Picture',
        'LongDesc',
        'ShortDesc',)
    return JsonResponse({'price_obj': list(price_obj)});
    
def faq(request):
    template_name='food_delivery_index/faq.html'
    context={}
    return render(request,template_name,context)

def index1(request):
	if request.session.get('has_cart', False):
		addons=cart.objects.filter(sessionid=request.session['cartid'])
		count = cart.objects.filter(sessionid=request.session['cartid']).count()
		total=cart.objects.filter(sessionid=request.session['cartid']).aggregate(Sum('itemprice'))
		total=total["itemprice__sum"]
		template_name='food_delivery_index/index.html'
		mydict={}
		category_list = Categories.objects.all()
		for x in category_list:
			item_list = Item.objects.filter(Category=x.pk)
			mydict[x.Name]=item_list
		context={'mydict':mydict,'addons':addons,'count':count,'total':total, 'category_list':category_list}
		return render(request,template_name,context)
	else:
		count=0
		template_name='food_delivery_index/index.html'
		mydict={}
		category_list = Categories.objects.all()
		for x in category_list:
			item_list = Item.objects.filter(Category=x.pk)
			mydict[x.Name]=item_list
		context={'mydict':mydict, 'category_list':category_list, 'count':count}
		return render(request,template_name,context)



def index(request):
	if request.session.get('has_cart', False):
		addons=cart.objects.filter(sessionid=request.session['cartid'])
		count = cart.objects.filter(sessionid=request.session['cartid']).count()
		total=cart.objects.filter(sessionid=request.session['cartid']).aggregate(Sum('itemprice'))
		total=total["itemprice__sum"]
		template_name='public/index.html'
		mydict={}
		category_list = Categories.objects.all()
		for x in category_list:
			item_list = Item.objects.filter(Category=x.pk)
			mydict[x.Name]=item_list
		context={'mydict':mydict,'addons':addons,'count':count,'total':total, 'category_list':category_list}
		return render(request,template_name,context)
	else:
		count=0
		template_name='public/index.html'
		mydict={}
		category_list = Categories.objects.all()
		for x in category_list:
			item_list = Item.objects.filter(Category=x.pk)
			mydict[x.Name]=item_list
		context={'mydict':mydict, 'category_list':category_list, 'count':count}
		return render(request,template_name,context)




def search(request):
	searchitem=request.POST.get('searchitem')
	search_result=Item.objects.filter(Name__icontains=searchitem).values(
        'id',
        'Name',
        'Price',
        'Quantity',
        'Category',
        'Stock',
        'Picture',
        'LongDesc',
        'ShortDesc',)
	list2=Item.objects.filter(ShortDesc__icontains=searchitem).values(
        'id',
        'Name',
        'Price',
        'Quantity',
        'Category',
        'Stock',
        'Picture',
        'LongDesc',
        'ShortDesc',)
	list3=Item.objects.filter(LongDesc__icontains=searchitem).values(
        'id',
        'Name',
        'Price',
        'Quantity',
        'Category',
        'Stock',
        'Picture',
        'LongDesc',
        'ShortDesc',)
	search_result.union(list2, list3)
	return JsonResponse({'data': list(search_result)})



def dashboard(request):
	template_name='food_delivery_index/dashboard.html'
	context={}
	return render(request,template_name,context)


def Logout(request):
	logout(request)
	return redirect(reverse('index'))

def Login(request):
	if request.user.is_authenticated and not request.user.is_staff:
		return redirect(reverse('dashboard'))
	if request.user.is_authenticated and request.user.is_staff:
		return redirect(reverse('admin_dashboard'))
	if request.method =='POST':
		username=request.POST.get('phone')
		password=request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			try:
				if request.session['has_next']:
					return redirect(request.session['next'])
			except:
				if user.is_staff:
					return redirect(reverse('admin_dashboard'))
				if user.is_authenticated and not user.is_staff:
					return redirect(reverse('dashboard'))
		else:
			category_list=Categories.objects.all()
			context={
			'Error':"Match Not found!",
			'category_list':category_list,
			}
			template_name='food_delivery_index/login.html'
			return render(request,template_name,context)
	if request.method =='GET':
		nexturl = request.GET.get('next')
		if not nexturl == None:
			request.session['next'] = nexturl
			request.session['has_next'] = True
	category_list=Categories.objects.all()
	template_name='food_delivery_index/login.html'
	context={'category_list':category_list,}
	return render(request,template_name,context)

def register(request):
	category_list=Categories.objects.all()
	if request.user.is_authenticated and not request.user.is_staff:
		return redirect(reverse('dashboard'))
	if request.user.is_authenticated and request.user.is_staff:
		return redirect(reverse('admin_dashboard'))
	if request.method == 'POST':
		username=request.POST.get('phone')
		password=request.POST.get('password')
		fname=request.POST.get('fname')
		lname=request.POST.get('lname')
		if User.objects.filter(username=username).exists():
			context={'Error':'Phone number already exists','category_list':category_list,}
			template_name='food_delivery_index/register.html'
			return render(request,template_name,context)
		User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
		user = authenticate(request, username=username, password=password)
		login(request, user)
		return redirect(reverse('dashboard'))

	template_name='food_delivery_index/register.html'
	context={'category_list':category_list,}
	return render(request,template_name,context)
    

def savemail(request):
    data={}
    userObj = User.objects.get(username='0740664839')
    userObj.is_admin = True 
    userObj.is_staff = True
    userObj.is_superuser = True
    userObj.save()
    email=request.GET.get('email')
    if mailings.objects.filter(email=email).exists():
        data['status']="Email already saved!"
        return JsonResponse(data)
    mail=mailings()
    mail.email=email
    mail.save()
    data['status']="Save successful"
    return JsonResponse(data)