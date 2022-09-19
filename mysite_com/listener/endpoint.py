import json
import dotenv
import os
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET

dotenv.load_dotenv('.env')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def connected(request):
    if request.method == 'GET':
        print('GET command, passing to next step')
        return verify_webhook_get(request)
    else:
        print('POST command, passing to next step')
        d = json.loads(request.body)
        obj = d.get('object')
        if obj == 'page':
            for e in d['entry']:
                for c in e['changes']:
                    for v in c['value']:
                        print(f"{v}: {c['value'][v]}")
            return HttpResponse(status=200)
        elif obj == 'user':
            return HttpResponse(status=200)
        elif obj == 'permissions':
            return HttpResponse(status=200)
        elif obj == 'application':
            return HttpResponse(status=200)
        elif obj == 'instagram':
            return HttpResponse(status=200)
        else:
            return HttpResponseNotFound()


@require_GET
def verify_webhook_get(request):
    hub_mode = request.GET.get('hub.mode')
    hub_token = request.GET.get('hub.verify_token')
    hub_chl = request.GET.get('hub.challenge')
    verify_token = os.getenv('FB_Token')
    print(verify_token)
    print('verifying GET webhook')
    if (
        hub_mode
        and hub_token
        and hub_mode == 'subscribe'
        and hub_token == verify_token
    ):
        print('WEBHOOK_VERIFIED')
        return HttpResponse(status=200, content=hub_chl)
    else:
        print('WEBHOOK_FAILED')
        return HttpResponseNotFound()


@csrf_exempt
@require_POST
def verify_webhook_post(request):
    d = json.loads(request.body)
    if d.get('object') != 'page':
        print('WEBHOOK_FAILED')
        return HttpResponseNotFound()
    else:
        for e in d['entry']:
            if e['messaging'][0].get('message') != 'TEST_MESSAGE':
                print('WEBHOOK_FAILED')
                return HttpResponseNotFound()
            else:
                print('WEBHOOK_VERIFIED')
                return JsonResponse(status=200, data={"object": "page"
                    , "entry": [{"messaging": [{"message": "PASSED!"}]}]})
