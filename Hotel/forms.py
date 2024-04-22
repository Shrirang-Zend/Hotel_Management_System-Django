from django import forms

class AvailabilityForm(forms.Form):
    room_categories = (
        ('YAC', 'AC Room'),
        ('NAC', 'Non AC Room'),
        ('DEL', 'Deluxe Suite'),
        ('KIN', 'King Suite'),
        ('QUE', 'Queen Suite'),
        ('NAU', 'Naukar Room'),
    )
    room_category = forms.ChoiceField(choices=room_categories, required=True)
    Check_In_Time = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M"])
    Check_Out_Time = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M"])