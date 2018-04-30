from django import forms
from django.contrib.auth import get_user_model
from .models import Task, SubTask

User=get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False

        if commit:
            user.save()
            user.profile.send_activation_email()
        return user

class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields =[
            'name',
            'description',
            'status',
        ]

class SubTaskCreateForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields =[
            'task',
            'description',
            'status',
        ]
        def __init__(self, user=None, *args, **kwargs):
            super(SubTaskForm, self).__init__(*args, **kwargs)
            self.fields['task'].queryset = Task.objects.filter(assigned=user)
