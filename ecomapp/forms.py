from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
import re


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields["username"].label = "Login"
		self.fields["password"].label = "Password"

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		if not User.objects.filter(username=username).exists():			
			raise forms.ValidationError('User not found')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Wrong password')


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
		    'username',
		    'password',
		    'password_check',
		    'first_name',
		    'last_name',
		    'email',
		]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields["username"].label = "Login"
		self.fields["password"].label = "Password"
		self.fields["password"].help_text = "Create password"
		self.fields["password_check"].label = "Repeat password"
		self.fields["first_name"].label = "First Name"
		self.fields["last_name"].label = "Last Name"
		self.fields["email"].label = "E-mail"
		self.fields["email"].help_text = "Please, enter valid mail!"

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']

		if User.objects.filter(username=username).exists():			
			raise forms.ValidationError('Login is already in use')
		if User.objects.filter(email=email).exists():			
			raise forms.ValidationError('User with entered email already exists')
		if password != password_check:
			raise forms.ValidationError('Passwords do not match')
		if re.search(r"[0-9]", password) is None : 
			if re.search(r"[A-Z]", "password") is None :
				raise forms.ValidationError('Password must contain at least one digit')


class OrderForm(forms.Form):

	name = forms.CharField()
	last_name = forms.CharField(required=False)
	phone = forms.CharField()
	buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Pick up from store"), ("delivery", "Delivery")]))
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	address = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)

	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields["name"].label = "First Name"
		self.fields["last_name"].label = "Last Name"
		self.fields["phone"].label = "Phone"
		self.fields["phone"].help_text = "Please, enter valid phone number!"
		self.fields["buying_type"].label = "Delivery Method"
		self.fields["address"].label = "Delivery Address"
		self.fields["address"].help_text = "Please, specify your locality / city!"
		self.fields["comments"].label = "Comments"
		self.fields["date"].label = "Delivery time"
		self.fields["date"].help_text = "Delivery is made the next day after placing the order. Our manager will contact you to clarify the details."
