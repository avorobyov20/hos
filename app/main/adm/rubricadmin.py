from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from adminsortable2.admin import SortableAdminMixin
from main.model.rubric import SubRubric
from main.forms.subrubric import SubRubricForm


class SubRubricInline(SortableInlineAdminMixin, admin.TabularInline):
    """33.2 Инструменты для администрирования рубрик
    Для надрубрик мы создадим встроенный редактор, чтобы пользователь,
    добавив новую надрубрику, смог сразу же заполнить ее подрубриками.
    Из формы для ввода и правки надрубрик исключим поле super_rubric,
    поскольку оно совершенно не нужно и будет только сбивать с толку."""

    model = SubRubric
    ordering = ["order"]


class SuperRubricAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Класс редактора для SuperRubric включает в себя
    встроенный редактор SubRubricInline."""

    exclude = ("super_rubric", "note")
    inlines = (SubRubricInline,)
    sortable_by = ()


class SubRubricAdmin(admin.ModelAdmin):
    """У подрубрик делаем поле super_rubric обязательным для заполнения.
    Для этого объявим форму SubRubricForm в form.py"""

    form = SubRubricForm
