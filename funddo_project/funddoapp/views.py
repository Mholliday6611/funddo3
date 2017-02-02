from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from models import UserProfile, Request
from django.contrib.auth.models import User
from forms import RequestForm, UserForm, UserFunderForm, ContactForm, UserJobSeekerForm, PasswordRecoveryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from braces.views import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views.generic import FormView
import urllib2
import json
# Create your views here.

def index(request):
	context_dict = {}
	request_list = Request.objects.order_by('-posted_on')[:10]

	context_dict['recent_requests']= request_list
	
	return render(request, 'index.html', context_dict)

def userbylocation(request):
	context_dict = {}
	user_location = UserProfile.objects.order_by('your_location')

	context_dict['user_location']= user_location
	
	return render(request, 'user_location.html', context_dict)
def about(request):
	context_dict = {}
	return render(request, 'about.html', context_dict)
@login_required
def make_request(request):
	if request.method == "POST":
		form = RequestForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.poster = request.user
			post.posted_on = datetime.now()
			post.email = request.POST['email']
			post.save()
			return HttpResponseRedirect('/')
	else:
		form = RequestForm()
	return render(request, 'make_request.html', {'form': form})

def requests(request, req_id):
	req = get_object_or_404(Request, id=req_id)
	email_post = req.email
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			form.EmailMessage(email_post)

			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = ContactForm()
	try:
		requested_post = request.objects.get()
	except:
		(Request.DoesNotExist)
	return render(request, 'requests.html', {'req': req, 'form': form}
		)

def register(request):
	context_dict = {}
	return render(request, 'register.html', context_dict)
	
def register_jobseeker(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserJobSeekerForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save() 

			profile = profile_form.save(commit=False)
			profile.jobseeker = True

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserJobSeekerForm()

	return render(request, 'register_jobseeker.html', {'user_form' : user_form, 'profile_form': profile_form, 'registered': registered})

def register_funder(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserFunderForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save() 

			profile = profile_form.save(commit=False)
			profile.funder = True

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserFunderForm()

	return render(request, 'register_funder.html', {'user_form' : user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse('Your account is inactive')
		else:
			print "Invalid login details : {0},{1}".format(username, password)
			return HttpResponse('Your login credentials were wrong')

	else:
		return render(request, 'login.html', {})
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def user_profile(request, user_username):
	context_dict = {}
	user = User.objects.get(username=user_username)
	profile = UserProfile.objects.get(user=user)
	context_dict['profile'] = profile
	context_dict['requests'] = Request.objects.filter(poster=user)

	return render(request, 'profile.html', context_dict)
@login_required
def edit_funderprofile(request, user_username):
	profile = get_object_or_404(UserProfile, user__username=user_username)
	services = profile.services
	pic = profile.picture
	bio = profile.bio
	if request.user != profile.user:
		return HttpResponse('Access Denied Loser')

	if request.method == 'POST':
		form = UserFunderForm(data=request.POST)
		if form.is_valid():
			if request.POST['services'] and request.POST['services'] != '':
				profile.services = request.POST['services']
			else:
				profile.services = services

			if request.POST['bio'] and request.POST['bio'] != '':
				profile.bio = request.POST['bio']
			else:
				profile.bio = bio

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			else:
				profile.picture = pic

			profile.save()

			return user_profile(request, profile.user.username)

		else:
			print form.errors
	else:
		form = UserFunderForm()
	return render(request, 'edit_funderprofile.html', {'form':form, 'profile':profile}) 

def edit_jobseekerprofile(request, user_username):
	profile = get_object_or_404(UserProfile, user__username=user_username)
	pic = profile.picture
	bio = profile.bio
	if request.user != profile.user:
		return HttpResponse('Access Denied Loser')

	if request.method == 'POST':
		form = UserJobSeekerForm(data=request.POST)
		if form.is_valid():

			if request.POST['bio'] and request.POST['bio'] != '':
				profile.bio = request.POST['bio']
			else:
				profile.bio = bio

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			else:
				profile.picture = pic

			profile.save()

			return user_profile(request, profile.user.username)

		else:
			print form.errors
	else:
		form = UserJobSeekerForm()
	return render(request, 'edit_jobseekerprofile.html', {'form':form, 'profile':profile}) 

class SettingsView(LoginRequiredMixin, FormView):
	template_name = 'settings.html'
	form_class = PasswordChangeForm
	success_url = reverse_lazy('index')

	def get_form(self, form_class):
		return form_class(user=self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self, request, form.user)
		return super(SettubgView, self).form_valid(form)

class PasswordRecoveryView(FormView):
	template_name = "password-recovery.html"
	form_class = PasswordRecoveryForm
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		form.reset_email()
		return super(PasswordRecoveryView, self).form_valid(form)
def gallery(request):
	url = "https://www.instagram.com/fund_dos/media/"
	json_obj=urllib2.urlopen(url)
	data = json.load(json_obj)
	images = []
	for i in data ['items']:
		images.append(i['images']['standard_resolution']['url'])
	return render(request, 'gallery.html',{'images':images})