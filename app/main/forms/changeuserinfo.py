from django import forms
from main.models import AdvUser


class ChangeUserInfoForm(forms.ModelForm):
    """Объявим форму, связанную с моделью AdvUser и предназначенную для
    ввода основных данных. Так как мы хотим сделать поле email модели AdvUser
    обязательным для заполнения то выполним полное объявление поля email формы,
    а поскольку параметры остальных полей формы username, first_name, last_name
    send_messages не меняются, то в их отношении применим быстрое объявление"""

    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = AdvUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )
