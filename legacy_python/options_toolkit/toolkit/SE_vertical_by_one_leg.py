from django.http import HttpResponse

def load_main_view(request):
    return HttpResponse("You are at: " + request.build_absolute_uri())
