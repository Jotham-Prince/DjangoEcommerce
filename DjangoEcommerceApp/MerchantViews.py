from django.views import View
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import HttpResponse
from .models import Service, ServiceMedia
from django.views.generic import ListView,View
from DjangoEcommerceApp.models import Categories,SubCategories,MerchantUser,Products,ProductAbout,ProductDetails,ProductMedia,ProductTransaction,ProductTags,CustomerOrders,CustomerUser
from django.core.files.storage import FileSystemStorage
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from DjangoEcommerce.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


class ProductView(View):
    def get(self,request,*args,**kwargs):
        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        merchant_users=MerchantUser.objects.filter(auth_user_id__is_active=True)

        return render(request,"merchant/product_create.html",{"categories":categories_list,"merchant_users":merchant_users})

    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")

        subcat_obj=SubCategories.objects.get(id=sub_category)
        merchant_user_obj=MerchantUser.objects.get(id=added_by_merchant)
        product=Products(product_name=product_name,in_stock_total=in_stock_total,url_slug=url_slug,brand=brand,subcategories_id=subcat_obj,product_description=product_description,product_max_price=product_max_price,product_discount_price=product_discount_price,product_long_description=long_desc,added_by_merchant=merchant_user_obj)
        product.save()

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        
        j=0
        for title_title in title_title_list:
            product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
            product_details.save()
            j=j+1

        for about in about_title_list:
            product_about=ProductAbout(title=about,product_id=product)
            product_about.save()
        
        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        product_transaction=ProductTransaction(product_id=product,transaction_type=1,transaction_product_count=in_stock_total,transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        return HttpResponse("OK")

@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+BASE_URL+''+file_url+'"}')



class ProductListView(ListView):
    model=Products
    template_name="merchant/product_list.html"
    paginate_by=4

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Products.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
            products=Products.objects.all().order_by(order_by)
        
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1,is_active=1).first()
            product_list.append({"product":product,"media":product_media})

        return product_list

    def get_context_data(self,**kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Products._meta.get_fields()
        return context


class ProductEdit(View):

    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_details=ProductDetails.objects.filter(product_id=product_id)
        product_about=ProductAbout.objects.filter(product_id=product_id)
        product_tags=ProductTags.objects.filter(product_id=product_id)

        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        return render(request,"merchant/product_edit.html",{"categories":categories_list,"product":product,"product_details":product_details,"product_about":product_about,"product_tags":product_tags})

    def post(self,request,*args,**kwargs):
        
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        title_title_list=request.POST.getlist("title_title[]")
        details_ids=request.POST.getlist("details_id[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        about_ids=request.POST.getlist("about_id[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")
        subcat_obj=SubCategories.objects.get(id=sub_category)

        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product.product_name=product_name
        product.url_slug=url_slug
        product.brand=brand
        product.subcategories_id=subcat_obj
        product.product_description=product_description
        product.product_max_price=product_max_price
        product.product_discount_price=product_discount_price
        product.product_long_description=long_desc
        product.save()

        
        j=0
        for title_title in title_title_list:
            detail_id=details_ids[j]
            if detail_id == "blank" and title_title!="":
                product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
                product_details.save()
            else: 
                if title_title!="":               
                    product_details=ProductDetails.objects.get(id=detail_id)
                    product_details.title=title_title
                    product_details.title_details=title_details_list[j]
                    product_details.product_id=product
                    product_details.save()
            j=j+1


        k=0
        for about in about_title_list:
            about_id=about_ids[k]
            if about_id=="blank" and about!="":
                product_about=ProductAbout(title=about,product_id=product)
                product_about.save()
            else:
                if about!="":
                    product_about=ProductAbout.objects.get(id=about_id)
                    product_about.title=about
                    product_about.product_id=product
                    product_about.save()
            k=k+1
        
        ProductTags.objects.filter(product_id=product_id).delete()

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        return HttpResponse("OK")

class ProductAddMedia(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"merchant/product_add_media.html",{"product":product})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        
        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        
        return HttpResponse("OK")

class ProductEditMedia(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_medias=ProductMedia.objects.filter(product_id=product_id)
        return render(request,"merchant/product_edit.html",{"product":product,"product_medias":product_medias})

class ProductMediaDelete(View):
    def get(self,request,*args,**kwargs):
        media_id=kwargs["id"]
        product_media=ProductMedia.objects.get(id=media_id)
        import os
        from DjangoEcommerce import settings
        os.remove(settings.MEDIA_ROOT.replace("\media","")+str(product_media.media_content).replace("/","\\"))
        
        product_id=product_media.product_id.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))

class ProductAddStocks(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"merchant/product_add_stocks.html",{"product":product})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product=Products.objects.get(id=product_id)
        old_stocks=product.in_stock_total
        new_stocks=int(new_instock)+int(old_stocks)
        product.in_stock_total=new_stocks
        product.save()

        product_obj=Products.objects.get(id=product_id)
        product_transaction=ProductTransaction(product_id=product_obj,transaction_product_count=new_instock,transaction_description="New Product Added",transaction_type=1)
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_add_stocks",kwargs={"product_id":product_id}))


from django.contrib.auth.decorators import login_required
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Products.objects.get(pk=product_id)
        quantity = request.POST.get('quantity', 1)
        user = request.user
        if user.user_type == 3:  # Ensure the user is a customer
            customer_user, created = CustomerUser.objects.get_or_create(auth_user_id=user)
            order = CustomerOrders.objects.create(
                product_id=product,
                user_id=customer_user,
                product_max_price=product.product_max_price,
                coupon_code='', 
                discount_amt=0,  
                product_status='In Cart',  
                quantity=quantity,  
            )
            order.save()
            return redirect('cart')  
        else:
            # Handle the case where the user is not a customer
            # Redirect to a different page or show an error message
            return redirect(reverse_lazy('product_list'))
            

@login_required
def update_cart(request):
    if request.method == 'POST':
        
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                order_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    order = CustomerOrders.objects.get(id=order_id, product_status='In Cart')
                    order.quantity = quantity
                    order.save()
                except (ValueError, CustomerOrders.DoesNotExist):
                    
                    pass

    cart_items = CustomerOrders.objects.filter(
        product_status='In Cart',
        user_id=request.user.customeruser  # Filter by the current user
    )
    for item in cart_items:
        item.total = item.quantity * item.product_id.product_max_price
    cart_subtotal = sum(item.total for item in cart_items)
    discount_amount = 0  
    cart_total = cart_subtotal - discount_amount

    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'discount_amount': discount_amount,
        'cart_total': cart_total,
    }
    return render(request, 'customer/cart.html', context)


@login_required
def cart(request):
    if request.method == 'POST':
        
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                order_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    order = CustomerOrders.objects.get(id=order_id, product_status='In Cart')
                    order.quantity = quantity
                    order.save()
                except (ValueError, CustomerOrders.DoesNotExist):
                    
                    pass

    cart_items = CustomerOrders.objects.filter(
        product_status='In Cart',
        user_id=request.user.customeruser  # Filter by the current user
    )
    for item in cart_items:
        item.total = item.quantity * item.product_id.product_max_price
    cart_subtotal = sum(item.total for item in cart_items)
    discount_amount = 0  
    cart_total = cart_subtotal - discount_amount

    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'discount_amount': discount_amount,
        'cart_total': cart_total,
    }
    return render(request, 'customer/cart.html', context)

