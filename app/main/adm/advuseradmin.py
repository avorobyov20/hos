from django.contrib import admin
from main.utilities import send_activation_notification
import datetime


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, "Письма с требованиями отправлены")


send_activation_notifications.short_description = (
    "Отправка писем с требованиями активации"
)


class NonactivatedFilter(admin.SimpleListFilter):
    title = "Прошли активацию?"
    parameter_name = "actstate"

    def lookups(self, request, model_admin):
        return (
            ("activated", "Прошли"),
            ("threedays", "Не прошли более 3 дней"),
            ("week", "Не прошли более недели"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "activated":
            return queryset.filter(is_active=True, is_activated=True)
        elif val == "threedays":
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(
                is_active=False, is_activated=False, date_joined__date__lt=d
            )
        elif val == "week":
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(
                is_active=False, is_activated=False, date_joined__date__lt=d
            )


class AdvUserAdmin(admin.ModelAdmin):
    # в списке записей будем выводить строковое представление пользователя,
    # поле признака выполненной активации и временную метку регистрации
    list_display = ("__str__", "is_activated", "date_joined")

    # разрешаем выполнять поиск по логину пользователя, почте, имени и фамилии
    search_fields = ("username", "email", "first_name", "last_name")

    # для выполнения фильтрации пользователей, выполнивших активацию,
    # не выполнивших ее в течение трех дней и недели,
    # используем класс вспомогательный класс NonactivatedFilter
    list_filter = (NonactivatedFilter,)

    # явно указываем список полей,
    # которые должны выводиться в формах для правки пользователей
    fields = (  # выстраиваем и группируем поля в удобном порядке
        ("username", "email"),
        ("first_name", "last_name"),
        ("is_active", "is_activated"),
        ("is_staff", "is_superuser"),
        "groups",
        "user_permissions",
        ("last_login", "date_joined"),
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )  # два последних поля делаем доступными только для чтения

    # регистрируем действие, которое разошлет пользователям
    # письма с предписаниями выполнить активацию
    # в нем мы переберем всех выбранных пользователей
    # и для каждого, кто не выполнил активацию,
    actions = (
        send_activation_notifications,
    )  # вызовем функцию send_activation_notification из модуля .utilities
