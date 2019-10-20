from .models import Lecture
from django import forms
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
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

class QueryForm(forms.Form):
    CHOICES = (
        ('1', 'greater'),
        ('2', 'lesser'),
    )
    category = forms.ChoiceField(choices=CHOICES, required=True,
                label='Students with attendance &nbsp;')
    attendance = forms.FloatField(initial=70, required=True,
                label=' &nbsp; than &nbsp; ',
                validators=[MinValueValidator(0), MaxValueValidator(100)]
                )            
    # visible_fields = ('category', 'attendance')               

