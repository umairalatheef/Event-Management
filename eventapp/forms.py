from .models import Booking, Review
from django import forms
from django.core.exceptions import ValidationError
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_name', 'event_place', 'email', 'event_date', 'mobile_number', 'number_of_persons', 'description']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_place': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_persons': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < date.today():
            raise ValidationError("The event date cannot be in the past.")
        return event_date

    def calculate_total_cost(self):
        num_of_persons = self.cleaned_data.get('number_of_persons', 0)
        rate_per_person = 250
        return num_of_persons * rate_per_person

# forms.py


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating', 'satisfaction_level']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts...'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'satisfaction_level': forms.HiddenInput(),
        }
