from .models import Lecture
from django import forms
import datetime
from django.core.validators import MinValueValidator
from django.utils import timezone

class NewLectureForm(forms.ModelForm):
    duration = forms.DurationField(initial=datetime.timedelta(days=0, hours=1), 
                required=True, label='Duration', help_text="days hh:mm:ss", 
                validators=[MinValueValidator(datetime.timedelta(days=0, hours=1, minutes=0))])
    time = forms.DateTimeField(label='Time', 
                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                validators=[MinValueValidator(timezone.localtime())]
                )  
    class Meta:
        model = Lecture
        fields = ('time', 'duration', 'Class')                     
