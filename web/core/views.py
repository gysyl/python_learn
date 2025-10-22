from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, Django! 这是你的入门应用。")
