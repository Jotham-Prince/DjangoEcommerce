from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from DjangoEcommerceApp.models import CustomUser,MerchantUser
from .forms import SignUpForm, LoginForm
from django.core.mail import EmailMessage
from . tokens import generate_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect
from .models import Service, ServiceMedia, Booking
from .forms import ServiceForm, ServiceMediaForm, BookingForm
from django.utils import timezone


# email views


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        myuser= None
    if myuser is not None and generate_token.check_token(myuser, token):
           myuser.is_active = True
           myuser.save()
           login(request, myuser)
           return redirect('home2')
    else:
        return redirect(request, 'activation_failed.html')
    
def activateEmail(request, user, to_email):
    mail_subject = 'Actiavte your user account'
    message = render_to_string("template_activate_account.html",{
             'user' : user.username,
             'domain' : get_current_site(request).domain,
             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
             'token': generate_token.make_token(user),
             'protocol': 'https' if request.is_secure() else 'http'
             })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
     messages.success(request, f'Dear <b>{user}<b>, please go to your email <b>{to_email}<b> inbox and click on \
                      received activation link to comfirm and complete the registration. <b>Note<b> Check your spam folder')
    else:
         messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')

# Customer and Merchant views


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # The save method now handles creating related user type instances
            # Send activation email
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'User created. Please check your email to activate your account.')
            # Redirect to the same page
            return redirect(reverse('combined_auth'))  # Use the name of your combined view
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'customer/combined_auth_template.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Redirect user based on user_type
                if user.user_type == 3:  # Customer
                    login(request, user)
                    return redirect(reverse_lazy('combined_list'))
                elif user.user_type == 2:  # Merchant
                    login(request, user)
                    return redirect(reverse_lazy('product_view'))
                elif user.user_type == 1:  # Admin
                    login(request, user)
                    return redirect('admin')  # Redirect to admin dashboard
                else:
                    msg = 'User type is not recognized'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'customer/combined_auth_template.html', {'form': form, 'msg': msg})


def combined_auth_view(request):
    login_form = LoginForm(request.POST or None)
    signup_form = SignUpForm(request.POST or None, request.FILES or None)
    msg = None

    if request.method == 'POST':
        if 'login' in request.POST:
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Redirect based on user type
                    return redirect(reverse_lazy('combined_list'))
                else:
                    msg = 'Invalid credentials'
            else:
                msg = 'Error validating form'

        elif 'signup' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save()
                # Send activation email
                activateEmail(request, user, signup_form.cleaned_data.get('email'))
                messages.success(request, 'User created. Please check your email to activate your account.')
                return redirect('login_view')
            else:
                msg = 'Form is not valid'

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'msg': msg
    }
    return render(request, 'customer/combined_auth_template.html', context)

def LogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("combined_auth"))



# admin views

def admin(request):
    return render(request, 'Admin/admin.html')

def adminLogin(request):
    return render(request,"Admin/Admin_signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request,user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))

@login_required(login_url="/admin/")
def admin_home(request):
    return render(request,"Admin/Admin_dashboard.html")

# other views

def index(request):
    return render(request,'customer/test.html')

def index1(request):
    return render(request,'customer/testModel.html')

def index2(request):
    return render(request,'customer/product.html')

def blog(request):
 return render(request, 'customer/blog.html')

def about(request):
    return render(request, 'customer/about.html')

def contact(request):
    return render(request, 'customer/contact.html')

def shop(request):
    return render(request, 'customer/shop.html')

def cart(request):
    return render(request, 'customer/cart.html')


def checkout(request):
    return render(request, 'customer/checkout.html')

def faq(request):
    return render(request, 'customer/faq.html')

def wishlist(request):
    return render(request, 'customer/wishlist.html')

def shop(request):
    return render(request, 'customer/category_list.html')

def merchant(request):
    return render(request,'merchant/service_create.html') 

def contact_view(request):
    return render(request, "customer/contact.html")

def  about(request):
    return render(request, "customer/about.html") 
  
def category_list(request):
    return render(request, "customer/category_list.html")


# View to add a new service


def add_service(request):
    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        service_media_form = ServiceMediaForm(request.POST, request.FILES)
        if service_form.is_valid() and service_media_form.is_valid():
            service = service_form.save()
            service_media = service_media_form.save(commit=False)
            service_media.service_id = service
            service_media.save()
            return redirect('service_list')
    else:
        service_form = ServiceForm()
        service_media_form = ServiceMediaForm()
    return render(request, 'merchant/add_service.html', {'service_form': service_form, 'service_media_form': service_media_form})

# View to edit an existing service
def edit_service(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'merchant/edit_service.html', {'form': form})

# View to delete a service
def delete_service(request, pk):
    Service.objects.get(pk=pk).delete()
    return redirect('service_list')

# View to list all services
def service_list(request):
    services = Service.objects.all()
    return render(request, 'merchant/service_list.html', {'services': services})

# View to view service details

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service_media = ServiceMedia.objects.filter(service_id=service, media_type='image', is_active=1).first()
    return render(request, 'merchant/service_detail.html', {'service': service, 'service_media': service_media})

# View to create a booking
def create_booking(request, service_id):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=service_id)
        booking_date = request.POST.get('booking_date')
        additional_details = request.POST.get('additional_details')
        if service.remaining_slots > 0 and timezone.now() < service.scheduled_at:
            Booking.objects.create(
                service=service,
                booking_date=booking_date,
                additional_details=additional_details
            )
            service.booked_slots += 1
            service.save()
            # Redirect to a confirmation page or back to the service detail
            return redirect('booked_services_list')
        else:
            # Handle the case where there are no slots or the service is past its schedule
            pass
    # Redirect to the service detail page if not a POST request or booking is not possible
    return redirect('service_detail', pk=service_id)

def booked_services_list(request):
    bookings = Booking.objects.select_related('service').all()
    return render(request, 'merchant/booked_services_list.html', {'bookings': bookings})