from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from todo_app.models import Profile, Tasks

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class EditAdditionalProfileInfo(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'country', 'phone_no']

class ChangeDpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class ScheduleTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['task', 'date_due']

class MarkTaskasCompleteForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['task_completed']