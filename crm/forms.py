from django import forms

from .models import Activity, Lead, Note


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "source",
            "status",
            "property_interest",
            "budget",
            "assigned_to",
            "follow_up_date",
        ]

        widgets = {
            "follow_up_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Add a note about this lead...",
                }
            ),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity

        fields = [
            "activity_type",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Describe the activity...",
                }
            ),
        }