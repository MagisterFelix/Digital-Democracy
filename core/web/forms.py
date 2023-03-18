import hashlib
from datetime import date, timedelta

from django import forms


class LoginForm(forms.Form):

    passport = forms.IntegerField(
        label="Passport",
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={"autofocus": True, "autocomplete": "off"})
    )
    password = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

    def clean(self):
        passport = self.cleaned_data.get("passport")
        self.cleaned_data["passport"] = hashlib.sha256(str(passport).encode()).hexdigest()


class BallotCreationForm(forms.Form):

    title = forms.CharField(
        label="Title",
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"})
    )
    options = forms.CharField(
        label="Options",
        required=True,
        help_text="Provide options separated by comma",
        widget=forms.TextInput(attrs={"pattern": r"^(?!.*(?:^,|,$))(?=.*[,]).+$", "autocomplete": "off"})
    )
    end_date = forms.DateField(
        label="End date",
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": date.today() + timedelta(days=1),
                "max": date.today() + timedelta(days=14)
            }
        )
    )


class VoteForm(forms.Form):

    option = forms.ChoiceField(
        label="",
        choices=(),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        selected = kwargs.pop("selected", None)
        options = kwargs.pop("options", ())
        disabled = kwargs.pop("disabled", False)

        super(VoteForm, self).__init__(*args, **kwargs)

        self.fields["option"].choices = options
        self.fields["option"].initial = selected
        self.fields["option"].disabled = bool(selected) or disabled
