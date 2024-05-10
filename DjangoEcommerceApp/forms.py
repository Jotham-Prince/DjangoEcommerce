from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser, AdminUser, MerchantUser, CustomerUser
from .models import Service, ServiceMedia, Booking
from django.core.files.storage import FileSystemStorage


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'description', 'duration', 'price', 'available_slots', 'scheduled_at']

class ServiceMediaForm(forms.ModelForm):
    media_content = forms.ImageField(label='Select a file', help_text='max. 42 megabytes')

    class Meta:
        model = ServiceMedia
        fields = ['media_content']  # Removed 'media_type' from the fields

    def save(self, commit=True):
        instance = super(ServiceMediaForm, self).save(commit=False)
        instance.media_type = 'image'  # Set 'media_type' to 'image' automatically
        if commit:
            instance.save()
        return instance
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'booking_date', 'additional_details']



class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    user_type = forms.ChoiceField(
        choices=[(2, "Merchant"), (3, "Customer")],  # Exclude the Admin choice
        widget=forms.RadioSelect(),
        initial=3  # Set Customer as the default selection
    )
    profile_pic = forms.ImageField(
        required=False,  # Make it optional
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    company_name = forms.CharField(
        required=False,  # Only required for merchants
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    gst_details = forms.CharField(
        required=False,  # Only required for merchants
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        required=False,  # Only required for merchants
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'profile_pic','company_name', 'gst_details', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.save()
        

        profile_pic = None
        if 'profile_pic' in self.files:
            profile_pic_file = self.files['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic_file.name, profile_pic_file)
            profile_pic = filename

        if user.user_type == '2':
            MerchantUser.objects.create(
                auth_user_id=user,
                profile_pic=profile_pic,  # Assign the file name
                company_name=self.cleaned_data.get('company_name'),
                gst_details=self.cleaned_data.get('gst_details'),
                address=self.cleaned_data.get('address')
            )
        elif user.user_type == '3': 
            CustomerUser.objects.create(
                auth_user_id=user,
                profile_pic=profile_pic  # Assign the file name
            )
        return user