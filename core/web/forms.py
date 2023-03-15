import hashlib

from django import forms


class LoginForm(forms.Form):

    passport = forms.IntegerField(
        label="Passport",
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

    def clean(self):
        passport = self.cleaned_data.get("passport")

        if passport is not None:
            self.cleaned_data["passport"] = hashlib.sha256(str(passport).encode()).hexdigest()
