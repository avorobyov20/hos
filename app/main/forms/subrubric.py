from django import forms
from main.model.rubric import SuperRubric, SubRubric


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(),
        empty_label=None,
        required=True,
        label="Надрубрика",
    )
    # Убираем у раскрывающегося списка, с помощью которого пользователь
    # будет выбирать подрубрику, "пустой" пункт присваиванием empty_label=None.
    # т.е. даем понять что в это поле должно быть обязательно занесено значение

    class Meta:
        model = SubRubric
        exclude = ("order",)
