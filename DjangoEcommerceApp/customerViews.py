from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from DjangoEcommerceApp.models import Categories,Service,Products,ProductAbout,ProductDetails,ProductMedia,ProductTags,ServiceMedia
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from DjangoEcommerce.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class CombinedListView(View):
    template_name = "customer/combined_template.html"

    def get(self, request, *args, **kwargs):
        # Fetch products data
        filter_val = request.GET.get("filter", "")
        order_by = request.GET.get("orderby", "id")
        if filter_val != "":
            products = Products.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
            products = Products.objects.all().order_by(order_by)
        
        product_list = []
        for product in products:
            product_media = ProductMedia.objects.filter(product_id=product.id, media_type=1, is_active=1).first()
            product_list.append({"product": product, "media": product_media})

        # Fetch categories data
        if filter_val != "":
            categories = Categories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            categories = Categories.objects.all().order_by(order_by)
        
        services = Service.objects.all()
        service_list = []
        for service in services:
            service_media = ServiceMedia.objects.filter(service_id=service.id, media_type='image', is_active=1).first()
            service_list.append({"service": service, "media": service_media})

        # Combine context data
        context = {
            'product_list': product_list,
            'categories_list': categories,
            'MEDIA_URL': settings.MEDIA_URL,
            'service_list': service_list,
            
        }

        return render(request, self.template_name, context)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = get_object_or_404(Products, pk=product_id)
        product_media = ProductMedia.objects.filter(product_id=product_id, is_active=1).first()
        product_details = ProductDetails.objects.filter(product_id=product_id)
        product_about = ProductAbout.objects.filter(product_id=product_id)
        product_tags = ProductTags.objects.filter(product_id=product_id)

        return render(
            request,
            "customer/product.html",
            {
                "product": product,
                "product_media": product_media,  # Include the product media in the context
                "product_details": product_details,
                "product_about": product_about,
                "product_tags": product_tags,
            },
        )