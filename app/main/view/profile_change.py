from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from main.models import AdvUser
from main.forms.changeuserinfo import ChangeUserInfoForm
from django.contrib import messages
from django.utils.safestring import mark_safe

""" 32.3.1 Веб-страница правки основных сведений: логина, почты, реальных
имени и фамилии, признака оповещений. Контроллер страницы основных данных
должен выполнять правку записи модели, так что мы можем написать его на базе
высокоуровневого класса UpdateView. В процессе работы этот контроллер должен
извлечь из модели AdvUser запись, представляющую текущего пользователя,
для чего ему нужно предварительно получить ключ текущего пользователя.
Получить его можно из объекта request.user. Лучшее место для получения ключа
текущего пользователя - метод setup(), наследуемый всеми контроллерами-классами
от их общего суперкласса View. Этот метод выполняется в самом начале исполнения
контроллера-класса и получает объект запроса в качестве одного из параметров.
В переопределенном методе setup() мы извлечем ключ пользователя и сохраним его
в атрибуте user_id. Извлечение исправляемой записи выполним в методе
get_object(), который контроллер-класс унаследовал от примеси SingleObjectMixin
своего базового класса. В переопределенном методе get_object сначала учитываем
тот момент, что набор записей, из которого следует извлечь искомую запись,
может быть передан методу с параметром queryset, а может и не быть - в этом
случае набор записей следует получить вызовом метода get_queryset().
После этого, непосредственно ищем запись, представляющую текущего пользователя.
Примесь SuccessMessageMixin применяется для вывода всплывающих сообщений
об успешном выполнении операции. Зря мы, что ли, вставили в шаблон basic.html,
код выводящий сообщения {% bootstrap_messages %}"""


class ChangeUserInfoView(LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = "main/change_user_info.html"
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy("main:index")

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk

        if request.method == "POST":
            messages.add_message(
                request,
                messages.SUCCESS,
                mark_safe(
                    "Уважаемый пользователь <b>"
                    + request.user.username
                    + "</b><p>Ваши личные данные были изменены.</p>"
                ),
            )

        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
