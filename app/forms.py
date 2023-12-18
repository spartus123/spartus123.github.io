from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, \
    PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from app.models import Customer


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Vardas',widget=forms.TextInput(attrs={
        'autofocus':'True','class':'form-control'}))
    password = forms.CharField(label='Slaptažodis',widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password', 'class':'form-control'}))
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Vardas Pavardė',widget=forms.TextInput(attrs={
        'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(label='El. Paštas', widget=forms.EmailInput(attrs={
        'class':'form-control'}))
    password1 = forms.CharField(label='Slaptažodis', widget=forms.PasswordInput(attrs={
        'class':'form-control'}))
    password2 = forms.CharField(label='Patvirtinti Slaptažodį', widget=forms.PasswordInput(attrs={
        'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Senas Slaptazodis', widget=forms.PasswordInput(attrs={
        'autofocus':'True','autocomplete':'current-password','autocapitalize':'none','autocorrect':'off','class':'form-control'}))
    new_password1 = forms.CharField(label='Naujas Slaptazodis', widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Patvirtinti nauja Slaptazodi',
                                    widget=forms.PasswordInput(
        attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordresetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Naujas Slaptazodis', widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Patvirtinti nauja Slaptazodi',
                                    widget=forms.PasswordInput(
        attrs={'autocomplete':'current-password','class':'form-control'}))
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','zipcode','state','phone']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control', 'required':False}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
        }

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if zipcode and (len(str(zipcode)) != 5):
            raise forms.ValidationError("ZIP kodas turi būti 5 skaitmenų ilgio.")
        return zipcode

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Vardas Pavardė'
        self.fields['locality'].label = 'Adresas'
        self.fields['city'].label = 'Miestas'
        self.fields['zipcode'].label = 'Pašto kodas'
        self.fields['state'].label = 'Regionas'
        self.fields['phone'].label = 'Telefono numeris'