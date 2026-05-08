from django import forms

from apps.applications.models import Application


class BaseApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("full_name", "phone", "email", "comment")
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Иванов Иван", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 999 000-00-00", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "mail@example.ru", "autocomplete": "email"}),
            "comment": forms.Textarea(attrs={"placeholder": "Комментарий к заявке", "rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        if not phone and not email:
            raise forms.ValidationError("Укажите телефон или email, чтобы сотрудники могли связаться с вами.")
        return cleaned_data


class FeedbackForm(BaseApplicationForm):
    class Meta(BaseApplicationForm.Meta):
        widgets = {
            **BaseApplicationForm.Meta.widgets,
            "comment": forms.Textarea(attrs={"placeholder": "Напишите вопрос или сообщение", "rows": 5}),
        }
