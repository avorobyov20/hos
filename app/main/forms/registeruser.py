from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from main.apps import user_registered
from main.models import AdvUser


""" 32.4.1 Форма для занесения сведений о новом пользователе
Здесь мы также комбинируем быстрое и полное объявление полей.
Полное объявление используем для создания полей email, password1
и password2. В качестве дополнительного поясняющего текста
у первого пароля указываем текст, составленный из требований к паролям,
выдвигаемых всеми действующими валидаторами- новый юзер сразу увидит
полный список требований. В методе clean_password1() выполняем валидацию
пароля, введенного в первое поле. Проверять таким же образом password2
нет необходимости. Достаточно будет в методе clean() проверить совпадение
паролей. Эта проверка будет выполняться после валидации первого пароля.

В переопределенном методе save() при сохранении нового пользователя
заносим значения False в поля is_active и is_activated, сообщая фреймворку,
что этот пользователь еще не может выполнять вход на сайт.
Далее сохраняем в модели закодированный пароль и отправляем сигнал
user_registered, чтобы отослать пользователю письмо с требованием активации.
"""


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Пароль (повторно)",
        widget=forms.PasswordInput,
        help_text="Введите тот же самый пароль еще раз для проверки",
    )

    # https://stackoverflow.com/questions/52322148/django-validate-password-with-auth-password-validators
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error("password1", error)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Введенные пароли не совпадают", code="password_mismatch"
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(
            self.cleaned_data["password1"]
        )  # видимо эта функция отвечает за кодирование пароля
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )
