from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from main.models import AdvUser
from django.utils.safestring import mark_safe

""" 32.5 Класс-контроллер, удаляющий текущего пользователя, сделаем производным
от DeleteView. Здесь используются те же программные приемы, что и в контроллере
ChangeUserInfoView: в переопределенном методе setup() сохраняем ключ текущего
пользователя, а в переопределенном методе get_object() - отыскиваем по этому
ключу пользователя, подлежащего удалению. Перед удалением текущего пользователя
необходимо выполнить выход, что мы и делаем в переопределенном методе post().
В этом же методе создаем сообщение об успешном удалении пользователя"""


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "main/delete_user.html"
    success_url = reverse_lazy("main:index")

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.user.username
        logout(request)
        messages.add_message(
            request,
            messages.SUCCESS,
            mark_safe("Пользователь <b>" + username + "</b> удален."),
        )
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
