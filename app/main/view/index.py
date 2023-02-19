from django.shortcuts import render
from main.model.playlist import Playlist
from django.db.models import Q
from main.models import AdvUser


def index(request):
    user: AdvUser = request.user
    if user.is_authenticated:
        # все зафиналенные админские плейлисты и принадлежащие
        # текущему пользователю, если тот не является админом
        pls = (
            Playlist.objects.filter(
                (Q(user__username="admin") & ~Q(subrubric__name="#"))
                | (
                    ~Q(user__username="admin")
                    & Q(user__username=user.username)
                    & Q(subrubric__name="#")
                )
            )
            .values("pk", "name", "user", "subrubric", "subrubric__name")
            .order_by("-user_id", "-pos")
        )
    else:
        pls = (
            Playlist.objects.filter(
                Q(user__username="admin") & ~Q(subrubric__name="#")
            )
            .values("pk", "name", "user", "subrubric", "subrubric__name")
            .order_by("-pos")
        )

    subrubric_name_all = "%s (%d)" % (
        "UNCATEGORIZED",
        Playlist.objects.filter(
            Q(user__username="admin") & ~Q(subrubric__name="#")
        ).count(),
    )
    for pl in pls:
        if (
            pl["user"] == 1
        ):  # доходим до первого админского плейлиста, admin <--> 1
            context = {
                "pls": pls,
                "pl": Playlist.objects.get(pk=pl["pk"]),
                "rubric_pk": 0,  # 0 будет означать все категории кроме "#"
                "subrubric_name_all": subrubric_name_all,
            }
            break
        else:
            pl["name"] = str(
                Playlist.objects.get(pk=pl["pk"])
            )  # только у пользовательских листов показываем кол-во тр

    # кроме этого, в контексте будет присутствовать ключ 'rubrics'
    # = SubRubric.objects.filter(~Q(name="#")).all(), см. middlewares.py
    return render(request, "main/index.html", context)
