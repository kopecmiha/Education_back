from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
import json
import os
from django.core.files.storage import default_storage
import time, sys

def hello(request):
    user_list = str({"hello": "world"})
    user_list = json.loads(user_list)
    return JsonResponse({"result": user_list})

def users(request):
    user_list = [obj.json() for obj in list(User.objects.all())]
    return JsonResponse({"result": user_list})

def projects(request):
    count_on_page = int(request.GET.get('count'))
    page_number = int(request.GET.get('number'))
    if request.GET.get('creator'):
        filt = request.GET.get('creator')
        filtered_project = [obj.json() for obj in list(Project.objects.filter(creator=filt).all())]
    elif request.GET.get('name'):
        filt = request.GET.get('name')
        filtered_project = [obj.json() for obj in list(Project.objects.filter(name=filt).all())]
    elif request.GET.get('tags'):
        filtered_project = []
        list_project = [obj.json() for obj in list(Project.objects.all())]
        filt = request.GET.get('tags').split(',')
        for obj in list_project:
            if obj['tags']:
                for tag in obj['tags']:
                    if len(tag['name'])>0:
                        if tag['name'] in filt:
                            if obj not in filtered_project:
                                filtered_project.append(obj)
    filtered_project = filtered_project[(page_number - 1) * count_on_page:page_number * count_on_page]
    return JsonResponse({"result": filtered_project})

def status(request):
    status_list = [obj.json() for obj in list(User.objects.all())]
    return JsonResponse({"result": status})


def tags(request):
    tag_list = [obj.json() for obj in list(Tag.objects.all())]
    return JsonResponse({"result": tag_list})

def comments(request):
    def sorted_by_date(comment):
        return comment['date'];
    count_on_page = int(request.GET.get('count'))
    page_number = int(request.GET.get('number'))
    comments_list = [obj.json() for obj in list(Comment.objects.all())]
    comments_list = comments_list[(page_number-1)*count_on_page:page_number*count_on_page]
    comments_list = sorted(comments_list, key=sorted_by_date, reverse=True)
    return JsonResponse({"result": comments_list})

def events(request):
    comments_list = [obj.json() for obj in list(Event.objects.all())]
    return JsonResponse({"result": comments_list})

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
                     avatar_image='',
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
def get_user_email(request):
    if request.method == "POST":
        request = json.loads(request.body)
        email = request['email']
        user = User.objects.filter(email=email).first()
        return JsonResponse(user.json())
    else:
        return HttpResponse(status=405)

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
        request = json.loads(request.body)
        user_id = request['id']
        User.objects.filter(id=user_id).update(**request)
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
        tags = request['tags']
        r = Project(name=str(name),
                 description=str(description),
                 image='',
                 )
        r.save()
        r.creator.add(User.objects.filter(id=creator).first())
        r.save()
        for tag in tags:
            if len(Tag.objects.filter(name=tag).all()) == 0:
                some_tag = Tag(name=tag)
                some_tag.save()
        for tag in tags:
            r.tags.add(Tag.objects.filter(name=tag).first())
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
        request = json.loads(request.body)
        project_id = request['id']
        Project.objects.filter(id=project_id).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def update_project_image(request,id):
    project_id = id
    if request.FILES:
        the_file = request.FILES['image']
        upload_to = 'proj_img/'
        timing = "proj" + str(int(time.time()))
        path = default_storage.save(os.path.join(upload_to, timing + the_file.name), the_file)
        link = default_storage.url(timing+ the_file.name).replace('/posts/media/',"")
        dictionary = {'image':link}
        Project.objects.filter(id=project_id).update(**dictionary)
        return JsonResponse({'img_name': link})
    else:
        return HttpResponse(status=404)

@csrf_exempt
def delete_project(request,id):
    project_id = id
    Project.objects.filter(id=project_id).delete()
    return HttpResponse(status=200)

@csrf_exempt
def write_status(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        project = request['project']
        user = request['user']
        r = Status(name=str(name),
                 project=Project.objects.filter(id=project).first(),
                 user=User.objects.filter(id=user).first(),
                 )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_status(request,id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    status = {"statuses": [obj.json() for obj in list(Status.objects.filter(project=project).all())]}
    if status:
        return JsonResponse(status)
    else:
        return HttpResponse(status=404)

def get_user_status(request,id):
    user_id = id
    user = User.objects.filter(id=user_id).first()
    status = {"statuses": [obj.json() for obj in list(Status.objects.filter(user=user).all())]}
    if status:
        return JsonResponse(status)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def update_status(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Status.objects.filter(user=user,project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_status(request,user,project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Status.objects.filter(user=user,project=project).delete()
    return HttpResponse(status=200)

@csrf_exempt
def write_tag(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        if Tag.objects.filter(name=name).first():
            return HttpResponse(status=405)
        else:
            project = request['project']
            r = Tag(name=str(name))
            r.save()
            r.project.add(Project.objects.filter(id=project).first())
            r.save()
            return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)

@csrf_exempt
def write_comment(request):
    if request.method == "POST":
        request = json.loads(request.body)
        description = request['description']
        project = request['project']
        user = request['user']
        date = time.time()
        r = Comment(description=str(description),
                 project=Project.objects.filter(id=project).first(),
                 user=User.objects.filter(id=user).first(),
                 date = date
                 )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_comment(request,id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    comment = {"comments": [obj.json() for obj in list(Comment.objects.filter(project=project).all())]}
    if comment:
        return JsonResponse(comment)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def update_comment(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Comment.objects.filter(user=user,project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_comment(request,user,project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Comment.objects.filter(user=user,project=project).delete()
    return HttpResponse(status=200)



@csrf_exempt
def write_event(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        project = request['project']
        user = request['user']
        date = time.time()
        r = Event(name=str(name),
                 project=Project.objects.filter(id=project).first(),
                 user=User.objects.filter(id=user).first(),
                 date = date
                 )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_event(request,id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    event = {"events": [obj.json() for obj in list(Event.objects.filter(project=project).all())]}
    if event:
        return JsonResponse(event)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def get_user_event(request,id):
    user_id = id
    user = User.objects.filter(id=user_id).first()
    event = {"events": [obj.json() for obj in list(Event.objects.filter(user=user).all())]}
    if event:
        return JsonResponse(event)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def update_event(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Event.objects.filter(user=user,project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def delete_event(request,user,project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Event.objects.filter(user=user,project=project).delete()
    return HttpResponse(status=200)