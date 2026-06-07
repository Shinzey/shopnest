"""
Forms for ShopNest application.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    User, Shop, ShoppingList, ShoppingListItem, Order, Review, Address, Preference, Product
)


class UserRegistrationForm(UserCreationForm):
    """Registration form - Base class."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerRegistrationForm(UserRegistrationForm):
    """Registration form for customers."""
    pincode = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'})
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    village = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village (Optional)'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'pincode', 'city', 'village', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        user.pincode = self.cleaned_data['pincode']
        user.city = self.cleaned_data['city']
        user.village = self.cleaned_data.get('village', '')
        if commit:
            user.save()
        return user


class ShopOwnerRegistrationForm(UserRegistrationForm):
    """Registration form for shop owners."""
    pincode = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'})
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    village = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village (Optional)'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'pincode', 'city', 'village', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'shop_owner'
        user.pincode = self.cleaned_data['pincode']
        user.city = self.cleaned_data['city']
        user.village = self.cleaned_data.get('village', '')
        if commit:
            user.save()
        return user


class DeliveryAgentRegistrationForm(UserRegistrationForm):
    """Registration form for delivery agents."""
    pincode = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Pincode'})
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service City'})
    )
    village = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Village (Optional)'})
    )
    
    vehicle_type = forms.ChoiceField(
    choices=[
        ('bike', 'Bike'),
        ('auto', 'Auto'),
        ('scooter', 'Scooter')
    ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    vehicle_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'KL 07 AB 1234'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'pincode', 'city', 'village', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'delivery_agent'
        user.pincode = self.cleaned_data['pincode']
        user.city = self.cleaned_data['city']
        user.village = self.cleaned_data.get('village', '')
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Login form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class ProfileForm(forms.ModelForm):
    """User profile form."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ShopForm(forms.ModelForm):
    """Shop edit form with image upload."""
    class Meta:
        model = Shop
        fields = ('name', 'shop_type', 'address', 'city', 'village', 'pincode', 'logo', 'opening_time', 'closing_time', 'min_order', 'delivery_time')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop Name'}),
            'shop_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'min_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': 'Minimum Order Amount'}),
            'delivery_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Delivery Time (minutes)'}),
        }


class AddressForm(forms.ModelForm):
    """Address form."""

    latitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': '0.000001'
            }
        )
    )

    longitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': '0.000001'
            }
        )
    )

    class Meta:
        model = Address
        fields = (
            'address_type',
            'address',
            'latitude',
            'longitude',
            'is_primary'
        )

        widgets = {
            'address_type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'is_primary': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class ShoppingListForm(forms.ModelForm):
    """Shopping list form."""
    class Meta:
        model = ShoppingList
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }


class ShoppingListItemForm(forms.ModelForm):
    """Shopping list item form."""
    class Meta:
        model = ShoppingListItem
        fields = ('name', 'quantity', 'unit', 'estimated_price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., piece, kg, liter'}),
            'estimated_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class OrderForm(forms.ModelForm):
    """Order form."""
    class Meta:
        model = Order
        fields = ('address', 'payment_method')
        widgets = {
            'address': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """Review form."""
    class Meta:
        model = Review
        fields = ('rating', 'title', 'comment')
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Stars') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review'}),
        }


class ProductForm(forms.ModelForm):
    """Product form for shop owners to add/edit products."""
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'image', 'stock', 'sku', 'is_available')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Description'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category (e.g., Groceries, Snacks)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': 'Price (₹)'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Stock Quantity'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU (Stock Keeping Unit)'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
