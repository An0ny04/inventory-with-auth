from django.shortcuts import render ,  HttpResponse ,redirect , HttpResponseRedirect , get_object_or_404
from .forms import UserForm , ProfileForm , ProductsForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .models import Products , OrderItem , Order
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserForm(data = request.POST)
        profile = ProfileForm(data = request.POST)
        if form.is_valid() and profile.is_valid():
            user = form.save()
            username = form.cleaned_data.get(user.email)
            user.set_password(user.password)
            user.save()
            profile = profile.save(commit=False)
            profile.user=user
            profile.save()
            return redirect("login")
    else:
        form = UserForm()
        profile = ProfileForm()
    return render(request, 'users/register.html', {'form': form , 'profile':profile})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            if user.profile.role == 'Admin':
                login(request , user)
                
                return redirect('adminlogin')
            else:
                login(request , user)
                
                return redirect('userlogin')
        else:
            return render(request,"users/login.html")
    else:
        return render(request,"users/login.html")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def admin_login(request):
    current_user = request.user
    if current_user.profile.role == 'Admin':
        if request.method == 'POST':
            form = ProductsForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return redirect('adminlogin')
                
        else:
            form = ProductsForm()
            pro = Products.objects.exclude(quantity='0')
            
        return render(request, 'users/adminlogin.html', {'form': form , 'pr':pro})
    else:
        logout(request)
        return render(request,"users/login.html")

@login_required(login_url='/login')
def update_data(request,id):
    current_user = request.user
    if current_user.profile.role == 'Admin':
        if request.method == 'POST':
            pi = Products.objects.get(pk=id)
            form = ProductsForm(request.POST,request.FILES,instance=pi)
            if form.is_valid():
                form.save()
                return render(request, 'users/updateproduct.html',{'form':form})
        else:
            pi = Products.objects.get(pk=id)
            form = ProductsForm( instance=pi)
            return render(request, 'users/updateproduct.html',{'form':form})
    else:
        logout(request)
        return render(request,"users/login.html")


@login_required(login_url='/login')
def delete_data(request , id):
    if request.method == 'POST':
        pi = Products.objects.get(pk=id)
        pi.delete()
        return redirect('adminlogin')


@login_required(login_url='/login')
def user_login(request):
    current_user = request.user
    if current_user.profile.role == 'User': 
    # role = request.user.profile.role()
    # print(role)
        pro = Products.objects.exclude(status='Inactive')
        pro = Products.objects.exclude(quantity='0')
        return render(request, 'users/userlogin.html', { 'pr': pro})
    else:
        logout(request)
        return render(request,"users/login.html")

def  add_to_cart(request,id):
    item = get_object_or_404(Products, id=id)
    order_item , created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order =  order_qs[0]
        if order.items.exists():
            order_item.order_quantity += 1
            order_item.save()
        else:
            
            order.items.add()
    else:
        Order_date = timezone.now()
        order = Order.objects.create(user=request.user ,Order_date=Order_date)
        order.items.add(order_item)
    return redirect('userlogin')


@login_required(login_url='/login')
def OrderSummaryView(request):
    try:
        order = OrderItem.objects.filter(user=request.user)
        order1 = Order.objects.get(user=request.user)
        for each in order:
            print(each) 
        print(order1.get_total) 
        return render(request , 'users/mycart.html', {'object' : order , 'object1': order1})
    except ObjectDoesNotExist:
        return render(request , 'users/mycart.html')

