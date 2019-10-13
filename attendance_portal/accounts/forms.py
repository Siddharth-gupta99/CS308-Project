from django import forms
from django.contrib.auth.forms import UserCreationForm

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')
        labels = {
            'first_name': _('Name'),
            'username': _('ID'),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')
        labels = {
            'first_name': _('Name'),
            'username': _('ID'),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user