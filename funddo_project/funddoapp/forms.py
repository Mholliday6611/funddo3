from django import forms
from models import Request, UserProfile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from models import UserProfile
from funddoapp.location import *
from django.core.mail import send_mail, EmailMessage
from django.utils.crypto import get_random_string

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class UserJobSeekerForm(forms.ModelForm):
	your_location = forms.ChoiceField(choices= LOCATION_CHOICES, widget=forms.Select(), required=True)
	class Meta:
		model = UserProfile
		fields = ('picture', 'bio')
		exclude = ('funder', 'services', 'jobseeker' )

class UserFunderForm(forms.ModelForm):
	your_location = forms.ChoiceField(choices= LOCATION_CHOICES, widget=forms.Select(), required=True)
	class Meta:
		model = UserProfile
		fields = ('picture', 'services', 'bio')
		exclude = ('jobseeker', 'funder' )

class RequestForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter a title")
	request = forms.CharField(widget=forms.Textarea(), required=True)
	email = forms.EmailField(max_length=123, help_text="Enter Email here")


	class Meta:
		model = Request
		fields = ('title', 'request')
		exclude = ('poster',)

class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	subject = forms.CharField(required=True)
	body = forms.CharField(widget=forms.Textarea(), required=True)
	email = forms.CharField(widget=forms.EmailInput(), required=True)

	def EmailMessage(self, email_post):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		subject = self.cleaned_data['subject']
		body = self.cleaned_data['body']
		
		message = '''
			Subject: {subject}
			Message:
			Hey {name} is interested in your request
			{body}
			you can email them at {email}
			'''.format(name=name,
				email=email,
				subject=subject,
				body=body)
		email_msg = EmailMessage('Someone is interested',
		 message,
		 email,
		 [email_post])

		email_msg.send()


class PasswordRecoveryForm(forms.Form):
	email = forms.EmailField(required=False)

	def clean_email(self):
		try:
			return User.objects.get(email=self.cleaned_data['email'])
		except User.DoesNotExist:
			raise forms.ValidaionError("Can't find a user based on this email")
		return self.cleaned_data["mail"]

	def reset_email(self):
		user = self.cleaned_data['email']

		password = get_random_string(length = 8)

		user.set_password(password)

		user.save()

		body = """
				"sorry you are having issues with your account! Below is your username and password!

				Username: {username}
				Password: {password}

				You can login here: http://localhost:8000/login/
				you can change your password here: http://localhost:8000/settings.html

				""".format(username=user.username, password=password)

		pw_msg = EmailMessage('Your new password', body, 'Mholliday6611@gmail.com', [user.email])

		pw_msg.send()