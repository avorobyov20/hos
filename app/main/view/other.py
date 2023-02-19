from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist


def other_page(request, page):
    try:
        template = get_template("main/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
