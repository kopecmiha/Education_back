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
    user_list = [obj.json() for obj in list(User.objects.all())]
    return JsonResponse({"result": user_list})

def projects(request):
    project_list = [obj.json() for obj in list(Project.objects.all())]
    return JsonResponse({"result": project_list})


@csrf_exempt
def authorization(request):
    if request.method == "POST":
        request = json.loads(request.body)
        email = request['email']
        password = request['password']
        user = User.objects.filter(email=email).first()
        if user and user.password == password:
            return JsonResponse(user.json())
        else:
            return HttpResponse(status=403)


@csrf_exempt
def write_user(request):
    if request.method == "POST":
        request = json.loads(request.body)
        email = request['email']
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse(status=400)
        else:
            name = request['name']
            last_name = request['last_name']
            patronimyc = request['patronimyc']
            password = request['password']
            r = User(name=str(name),
                     last_name=str(last_name),
                     patronimyc=str(patronimyc),
                     email=str(email),
                     password=str(password),
                     avatar_image='download.jpeg',
                     )
            r.save()
            return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)

@csrf_exempt
def get_user(request,id):
    user_id = id
    user = User.objects.filter(id=user_id).first()
    if user:
        return JsonResponse(user.json())
    else:
        return HttpResponse(status=404)

@csrf_exempt
def delete_user(request,id):
    user_id = id
    User.objects.filter(id=user_id).delete()
    return HttpResponse(status=200)

@csrf_exempt
def delete_all(request):
    if request.method == "GET":
        #for i in User.objects.all():
        for i in Project.objects.all():
            i.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def update_user(request):
    if request.method == "POST":
        dictionary = request.POST.dict()
        request = json.loads(request.body)
        user_id = request['id']
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


@csrf_exempt
def write_project(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        description = request['description']
        creator = request['creator']
        r = Project(name=str(name),
                 description=str(description),
                 image='proekt-4.jpg',
                 )
        r.save()
        r.creator.add(User.objects.filter(id=creator).first())
        r.save()
        return JsonResponse(r.json())
        #return JsonResponse({"r":str(r)})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project(request,id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    if project:
        return JsonResponse(project.json())
    else:
        return HttpResponse(status=404)

@csrf_exempt
def update_project(request):
    if request.method == "POST":
        dictionary = request.POST.dict()
        request = json.loads(request.body)
        project_id = request['id']
        Project.objects.filter(id=project_id).update(**dictionary)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_project(request,id):
    project_id = id
    Project.objects.filter(id=project_id).delete()
    return HttpResponse(status=200)