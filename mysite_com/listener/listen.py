import re
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import endpoint


# noinspectilisteneron PyUnusedLocal
@csrf_exempt
@require_http_methods(["GET", "POST"])
def listener(request):
    i = request.get_host()
    if request.method in ['GET', 'POST']:
        print(f'redirecting {i} to graph')
        return endpoint.connected(request)
    else:
        print('unexpected method')
        return HttpResponseNotFound()