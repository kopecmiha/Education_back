from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
import json
import os
from django.core.files.storage import default_storage
import time

def hello(request):
    user_list = str({"hello": "world"})
    user_list = json.loads(user_list)
    return JsonResponse({"result": user_list})

def users(request):
    user_list = [json.loads(str(obj.__str__()).replace("\'", "\"")) for obj in list(User.objects.all())]
    return JsonResponse({"result": user_list})

@csrf_exempt
def write_user(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        last_name = request['last_name']
        patronimyc = request['patronimyc']
        type = request['type']
        organization = request['organization']
        email = request['email']
        password = request['password']
        r = User(name=str(name),
                 last_name=str(last_name),
                 patronimyc=str(patronimyc),
                 type=str(type),
                 email=str(email),
                 password=str(password),
                 organization=str(organization),
                 avatar_image='download.jpeg',
                 )
        r.save()
        return JsonResponse({"Response": r.__str__()})
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_user(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user_id = request['id']
        User.objects.filter(id=user_id).delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_all(request):
    if request.method == "GET":
        for i in User.objects.all():
            i.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def update_user(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user_id = request['id']
        dictionary = request.POST.dict()
        User.objects.filter(id=user_id).update(**dictionary)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def update_user_avatar2(request,id):
    user_id = id
    if request.FILES:
        the_file = request.FILES['image']
        upload_to = 'avatars/'
        timing = str(int(time.time()))
        path = default_storage.save(os.path.join(upload_to, timing + the_file.name), the_file)
        link = default_storage.url(timing+ the_file.name).replace('/posts/media/',"")
        dictionary = {'avatar_image':link}
        User.objects.filter(id=user_id).update(**dictionary)
        return JsonResponse({'img_name': link})
    else:
        return HttpResponse(status=404)