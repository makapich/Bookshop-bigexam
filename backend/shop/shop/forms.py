from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ModifiedUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)


class BookSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by title'})
    )


class UserAddressForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
