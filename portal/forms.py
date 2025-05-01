from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Donor, Receiver, Donation

# Donor Signup Form
class DonorSignupForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'donor'
        if commit:
            user.save()
            Donor.objects.create(user=user, mobile_number=self.cleaned_data['mobile_number'])
        return user


# Receiver Signup Form
class ReceiverSignupForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'receiver'
        if commit:
            user.save()
            Receiver.objects.create(user=user, mobile_number=self.cleaned_data['mobile_number'])
        return user


# Donor Login Form
class DonorLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Receiver Login Form
class ReceiverLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Donation Form
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['food_type', 'quantity', 'pickup_location', 'pickup_time', 'expiry_date']
        widgets = {
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'food_type': 'Type of Food',
            'quantity': 'Quantity',
            'pickup_location': 'Pickup Location',
            'pickup_time': 'Pickup Time',
            'expiry_date': 'Expiry Date',
        }

