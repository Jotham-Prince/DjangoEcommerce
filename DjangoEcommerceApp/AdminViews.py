from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from DjangoEcommerceApp.models import Categories,SubCategories,CustomUser,MerchantUser,Products,ProductAbout,ProductDetails,ProductMedia,ProductTransaction,ProductTags,CustomerUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from DjangoEcommerce.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="/admin/")
def admin_home(request):
    return render(request,"Admin/Admin_dashboard.html")

class CategoriesListView(ListView):
    model=Categories
    template_name="Admin/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Categories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Categories._meta.get_fields()
        return context


class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Categories
    success_message="Category Added!"
    fields="__all__"
    template_name="Admin/category_create.html"

class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="Admin/category_update.html"


class SubCategoriesListView(ListView):
    model=SubCategories
    template_name="Admin/sub_category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context


class SubCategoriesCreate(SuccessMessageMixin,CreateView):
    model=SubCategories
    success_message="Sub Category Added!"
    fields="__all__"
    template_name="Admin/sub_category_create.html"

class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="Admin/sub_category_update.html"

class MerchantUserListView(ListView):
    model=MerchantUser
    template_name="Admin/merchant_list.html"
    paginate_by=5

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=MerchantUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=MerchantUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(MerchantUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=MerchantUser._meta.get_fields()
        return context


class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    template_name="Admin/merchant_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]
    
    def form_valid(self, form):
        
    # Saving Custom User Object for Merchant User
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 2
        user.set_password(form.cleaned_data["password"])
        user.save()

        # Create MerchantUser instance
        merchant_user = MerchantUser(auth_user_id=user)
        merchant_user.save()

        # Now you can safely assign values to merchantuser fields
        profile_pic = self.request.FILES.get("profile_pic")
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            merchant_user.profile_pic = profile_pic_url

        merchant_user.company_name = self.request.POST.get("company_name")
        merchant_user.gst_details = self.request.POST.get("gst_details")
        merchant_user.address = self.request.POST.get("address")
    

        # Save the MerchantUser instance after assigning all fields
        merchant_user.save()

        messages.success(self.request, "Merchant User Created")
        return HttpResponseRedirect(reverse("merchant_list"))


class MerchantUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="Admin/merchant_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchantuser=MerchantUser.objects.get(auth_user_id=self.object.pk)
        context["merchantuser"]=merchantuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        merchantuser=MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            merchantuser.profile_pic=profile_pic_url

        merchantuser.company_name=self.request.POST.get("company_name")
        merchantuser.gst_details=self.request.POST.get("gst_details")
        merchantuser.address=self.request.POST.get("address")
        
      
        
        merchantuser.save()
        messages.success(self.request,"Merchant User Updated")
        return HttpResponseRedirect(reverse("merchant_list"))


class CustomerUserListView(ListView):
    model=CustomerUser
    template_name="Admin/customer_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=CustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=CustomerUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CustomerUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=CustomerUser._meta.get_fields()
        return context


class CustomerUserCreateView(SuccessMessageMixin,CreateView):
    template_name="Admin/customer_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        customeruser = CustomerUser(auth_user_id=user)
        customeruser.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        customeruser.profile_pic = profile_pic_url
        customeruser.save()

        # user.customeruser.profile_pic=profile_pic_url
        # user.save()
        messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("customer_list"))


class CustomerUserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = "Admin/customer_update.html"
    model = CustomUser
    fields = ["first_name", "last_name", "email", "username"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customeruser = CustomerUser.objects.get(auth_user_id=self.object.pk)
        context["CustomerUser"] = customeruser
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        # Update CustomerUser object if profile_pic is uploaded
        customeruser = CustomerUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic"):
            profile_pic = self.request.FILES["profile_pic"]
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            customeruser.profile_pic = profile_pic_url
            customeruser.save()

        messages.success(self.request, "Customer User Updated")
        return HttpResponseRedirect(reverse("customer_list"))
