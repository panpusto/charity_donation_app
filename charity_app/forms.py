from django import forms

from charity_app.models import Donation


class AddDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            "quantity",
            "categories",
            "institution",
            "address",
            "phone_number",
            "city",
            "zip_code",
            "pick_up_date",
            "pick_up_time",
            "pick_up_comment",
        ]
        widgets = {
            "quantity": forms.NumberInput(attrs={"step": 1, 'min': 1}),
            "categories": forms.CheckboxSelectMultiple(),
            "institution": forms.RadioSelect(),
            "phone_number": forms.TextInput(attrs={"type": "phone"}),
            "pick_up_date": forms.DateInput(attrs={"type": "date"}),
            "pick_up_time": forms.TimeInput(attrs={"type": "time"}),
            "pick_up_comment": forms.Textarea(attrs={"rows": 5})
        }
