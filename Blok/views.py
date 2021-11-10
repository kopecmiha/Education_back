from django.db.models import Q
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


def cards(request):
    user_list = [obj.json() for obj in list(Card.objects.all())]
    return JsonResponse({"result": user_list})


def projects(request):
    count_on_page = int(request.GET.get('count', default=100))
    page_number = int(request.GET.get('number', default=1))
    if request.GET.get('creator'):
        filt = request.GET.get('creator')
        filtered_project = [obj.json() for obj in list(Project.objects.filter(creator=filt).all())]
    elif request.GET.get('name'):
        filtered_project = []
        filt = request.GET.get('name').lower()
        project_list = [obj.json() for obj in list(Project.objects.all())]
        for obj in project_list:
            if filt in obj['name'].lower():
                filtered_project.append(obj)
    elif request.GET.get('category'):
        filt = request.GET.get('category')
        filtered_project = [obj.json() for obj in list(Project.objects.filter(category=filt).all())]
    elif request.GET.get('tags'):
        filtered_project = []
        list_project = [obj.json() for obj in list(Project.objects.all())]
        filt = request.GET.get('tags').split(',')
        for obj in list_project:
            if obj['tags']:
                for tag in obj['tags']:
                    if len(tag['name']) > 0:
                        if tag['name'] in filt:
                            if obj not in filtered_project:
                                filtered_project.append(obj)
    else:
        filtered_project = [obj.json() for obj in list(Project.objects.all())]
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
        return comment['date']

    count_on_page = int(request.GET.get('count'))
    page_number = int(request.GET.get('number'))
    comments_list = [obj.json() for obj in list(Comment.objects.all())]
    comments_list = comments_list[(page_number - 1) * count_on_page:page_number * count_on_page]
    comments_list = sorted(comments_list, key=sorted_by_date, reverse=True)
    return JsonResponse({"result": comments_list})


def activities(request):
    def sorted_by_date(comment):
        return comment['date']

    count_on_page = int(request.GET.get('count', default="100"))
    page_number = int(request.GET.get('number', default="1"))
    if request.GET.get('type'):
        filt = request.GET.get('type')
        filtered_activities = [obj.json() for obj in list(Activity.objects.filter(type=filt).all())]
    else:
        filtered_activities = [obj.json() for obj in list(Activity.objects.all())]
    filtered_activities = filtered_activities[(page_number - 1) * count_on_page:page_number * count_on_page]
    filtered_activities = sorted(filtered_activities, key=sorted_by_date, reverse=True)
    return JsonResponse({"result": filtered_activities})


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
def get_user(request, id):
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
def delete_user(request, id):
    user_id = id
    User.objects.filter(id=user_id).delete()
    return HttpResponse(status=200)


@csrf_exempt
def delete_all(request):
    if request.method == "GET":
        # for i in User.objects.all():
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
def update_user_avatar2(request, id):
    user_id = id
    if request.FILES:
        the_file = request.FILES['image']
        upload_to = 'avatars/'
        timing = str(int(time.time()))
        path = default_storage.save(os.path.join(upload_to, timing + the_file.name), the_file)
        link = default_storage.url(timing + the_file.name).replace('/posts/media/', "")
        dictionary = {'avatar_image': link}
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
        category = request['category']
        r = Project(name=str(name),
                    description=str(description),
                    image='',
                    category=str(category)
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
        # return JsonResponse({"r":str(r)})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project(request, id):
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
def update_project_image(request, id):
    project_id = id
    if request.FILES:
        the_file = request.FILES['image']
        upload_to = 'proj_img/'
        timing = "proj" + str(int(time.time()))
        path = default_storage.save(os.path.join(upload_to, timing + the_file.name), the_file)
        link = default_storage.url(timing + the_file.name).replace('/posts/media/', "")
        dictionary = {'image': link}
        Project.objects.filter(id=project_id).update(**dictionary)
        return JsonResponse({'img_name': link})
    else:
        return HttpResponse(status=404)


@csrf_exempt
def delete_project(request, id):
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
def get_project_status(request, id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    status = {"statuses": [obj.json() for obj in list(Status.objects.filter(project=project).all())]}
    if status:
        return JsonResponse(status)
    else:
        return JsonResponse({"statuses": []})


@csrf_exempt
def get_user_status(request, id):
    user_id = id
    count_on_page = int(request.GET.get('count', default=100))
    page_number = int(request.GET.get('number', default=1))
    user = User.objects.filter(id=user_id).first()
    status = [obj.json() for obj in list(Status.objects.filter(user=user).all())]
    filtered_project = status[(page_number - 1) * count_on_page:page_number * count_on_page]
    if status:
        return JsonResponse({"statuses": filtered_project})
    else:
        return JsonResponse({"statuses": []})


@csrf_exempt
def update_status(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Status.objects.filter(user=user, project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def delete_status(request, user, project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Status.objects.filter(user=user, project=project).delete()
    return HttpResponse(status=200)


@csrf_exempt
def write_tag(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        tag = Tag.objects.filter(name=name).first()
        if tag:
            project_id = request['project']
            project = Project.objects.filter(id=project_id).first()
            project.tags.add(tag)
            project.save()
            return HttpResponse(status=405)
        else:
            project_id = request['project']
            r = Tag(name=str(name))
            r.save()
            project = Project.objects.filter(id=project_id).first()
            project.tags.add(r)
            project.save()
            return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def write_recrut(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        project_id = request['project']
        r = Recrut(name=str(name))
        r.save()
        project = Project.objects.filter(id=project_id).first()
        project.recruts.add(r)
        project.save()
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
                    date=date
                    )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_comment(request, id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    comment = {"comments": [obj.json() for obj in list(Comment.objects.filter(project=project).all())]}
    if comment:
        return JsonResponse(comment)
    else:
        return JsonResponse({"comments": []})


@csrf_exempt
def update_comment(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Comment.objects.filter(user=user, project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def delete_comment(request, user, project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Comment.objects.filter(user=user, project=project).delete()
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
                  date=date
                  )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_event(request, id):
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    event = {"events": [obj.json() for obj in list(Event.objects.filter(project=project).all())]}
    if event:
        return JsonResponse(event)
    else:
        return JsonResponse({"events": []})


@csrf_exempt
def get_user_event(request, id):
    user_id = id
    user = User.objects.filter(id=user_id).first()
    event = {"events": [obj.json() for obj in list(Event.objects.filter(user=user).all())]}
    if event:
        return JsonResponse(event)
    else:
        return JsonResponse({"events": []})


@csrf_exempt
def update_event(request):
    if request.method == "POST":
        request = json.loads(request.body)
        user = User.objects.filter(id=request['user']).first()
        project = Project.objects.filter(id=request['project']).first()
        Event.objects.filter(user=user, project=project).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def delete_event(request, user, project):
    user = User.objects.filter(id=user).first()
    project = Project.objects.filter(id=project).first()
    Event.objects.filter(user=user, project=project).delete()
    return HttpResponse(status=200)


@csrf_exempt
def writecolumn(request):
    if request.method == "POST":
        request = json.loads(request.body)
        order = request['order']
        name = request['name']
        project_id = request['project_id']
        project = Project.objects.filter(id=project_id).first()
        column = Column(name=name,
                        order=order,
                        project=project
                        )
        column.save()
        return JsonResponse({"Response": column.json()})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def writecard(request):
    if request.method == "POST":
        request = json.loads(request.body)
        project_id = request['project_id']
        project = Project.objects.filter(id=project_id).first()
        name = request['name']
        description = request['description']
        column_order = request['column_order']
        order = request['order']
        date_start = request['date_start']
        date_finish = request['date_finish']
        if request['date_start']:
            date_start = request['date_start']
        if request['date_finish']:
            date_finish = request['date_finish']
        column = Column.objects.filter(project=project, order=column_order).first()
        card = Card(name=name,
                    description=description,
                    column=column,
                    order=order,
                    date_start=date_start,
                    date_finish=date_finish
                    )
        card.save()
        return JsonResponse({"Response": card.json()})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def getboard(request, id):
    final_columns = []
    project_id = id
    project = Project.objects.filter(id=project_id).first()
    columns = [obj.json() for obj in list(Column.objects.filter(project=project).all())]
    for col in columns:
        columna = Column.objects.filter(project=col['project']['id'], name=col['name']).first()
        col = col.update({
            'cards': [obj.json() for obj in list(Card.objects.filter(column=columna).all())]
        })
    if columns:
        return JsonResponse({"columns": columns})
    else:
        return JsonResponse({"columns": []})


@csrf_exempt
def switch(request):
    if request.method == "POST":
        request = json.loads(request.body)
        column_prev = request['column_order']
        card_prev = request['card_order']
        column_next = request['column_next']
        card_next = request['card_next']
        project_id = request['project_id']
        project = Project.objects.filter(id=project_id).first()
        column_start = Column.objects.filter(project=project, order=column_prev).first()
        column_finish = Column.objects.filter(project=project, order=column_next).first()
        card_start = Card.objects.filter(column=column_start, order=card_prev).first()
        for some_card in Card.objects.filter(column=column_start).all():
            if some_card.order > card_prev:
                some_card.order -= 1
                some_card.save()
        for some_card in Card.objects.filter(column=column_finish).all():
            if some_card.order >= card_next:
                some_card.order += 1
                some_card.save()
        card_start.order = card_next
        card_start.column = column_finish
        card_start.save()

        return JsonResponse({"Response": True})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def switch_columns(request):
    if request.method == "POST":
        request = json.loads(request.body)
        project = Project.objects.filter(id=request['project_id']).first()
        column_start = Column.objects.filter(project=project, order=request['column_start']).first()
        for column in Column.objects.filter(project=project).all():
            if request['column_start'] < request['column_finish']:
                if request['column_start'] < column.order <= request['column_finish']:
                    column.order -= 1
                    column.save()

            if request['column_start'] > request['column_finish']:
                if request['column_start'] > column.order >= request['column_finish']:
                    column.order += 1
                    column.save()
        column_start.order = request['column_finish']
        column_start.save()
        return JsonResponse({"Response": True})


@csrf_exempt
def write_active(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        description = request['description']
        project = request['project']
        user = request['user']
        date = time.time()
        type = request['type']
        link = ""
        if request['link']:
            link = request['link']
        r = Activity(name=str(name),
                     description=str(description),
                     project=Project.objects.filter(id=project).first(),
                     user=User.objects.filter(id=user).first(),
                     date=date,
                     type=type,
                     link=link
                     )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def write_money(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        description = request['description']
        stage = request['stage']
        user = request['user']
        date = time.time()
        sum = int(request['sum'])
        r = Money(name=str(name),
                  description=str(description),
                  stage=Stage.objects.filter(id=stage).first(),
                  user=User.objects.filter(id=user).first(),
                  date=date,
                  sum=sum
                  )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_stage_money(request, id):
    def sorted_by_date(money):
        return money['date']

    stage_id = id
    stage = Stage.objects.filter(id=stage_id).first()
    money = [obj.json() for obj in list(Money.objects.filter(stage=stage).all())]
    money_list = sorted(money, key=sorted_by_date, reverse=True)
    if money_list:
        return JsonResponse({'money': money_list})
    else:
        return JsonResponse({'money': []})


@csrf_exempt
def get_project_active(request, id):
    def sorted_by_date(active):
        return active['date']

    project_id = id
    project = Project.objects.filter(id=project_id).first()
    if request.GET.get('type'):
        filt = request.GET.get('type')
        active = [obj.json() for obj in list(Activity.objects.filter(project=project, type=filt).all())]
    else:
        active = [obj.json() for obj in list(Activity.objects.filter(project=project).all())]
    activities_list = sorted(active, key=sorted_by_date, reverse=True)
    if active:
        return JsonResponse({'activities': activities_list})
    else:
        return JsonResponse({'activities': []})


@csrf_exempt
def get_user_active(request, id):
    def sorted_by_date(active):
        return active['date']

    user_id = id
    user = User.objects.filter(id=user_id).first()
    active = [obj.json() for obj in list(Activity.objects.filter(user=user).all())]
    activities_list = sorted(active, key=sorted_by_date, reverse=True)
    if active:
        return JsonResponse({'activities': activities_list})
    else:
        return JsonResponse({'activities': []})


@csrf_exempt
def update_active_file(request, id):
    activity_id = id
    if request.FILES:
        the_file = request.FILES['image']
        upload_to = 'files/'
        timing = "act" + str(int(time.time()))
        path = default_storage.save(os.path.join(upload_to, timing + the_file.name), the_file)
        link = default_storage.url(timing + the_file.name).replace('/posts/media/', "")
        dictionary = {'file': link}
        Activity.objects.filter(id=activity_id).update(**dictionary)
        return JsonResponse(dictionary)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def write_active_comment(request):
    if request.method == "POST":
        request = json.loads(request.body)
        description = request['description']
        activity = request['activity']
        user = request['user']
        date = time.time()
        r = ActivityComment(
            description=str(description),
            activity=activity,
            user=user,
            date=date
        )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_active_comment(request, id):
    activity_id = id
    comment = {
        "activity_comments": [obj.json() for obj in list(ActivityComment.objects.filter(activity=activity_id).all())]}
    if comment:
        return JsonResponse(comment)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def update_active_comment(request):
    if request.method == "POST":
        request = json.loads(request.body)
        id = request['id']
        act = ActivityComment.objects.filter(id=id).update(**request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def delete_active_comment(request, id):
    ActivityComment.objects.filter(id=id).delete()
    return HttpResponse(status=200)


@csrf_exempt
def write_stage(request):
    if request.method == "POST":
        request = json.loads(request.body)
        name = request['name']
        description = request['description']
        project = request['project']
        period = request['period']
        date = time.time()
        r = Stage(
            name=str(name),
            description=str(description),
            project=str(project),
            period=str(period),
            date=date
        )
        r.save()
        return JsonResponse(r.json())
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_project_stage(request, id):
    project_id = id
    stage = {"stage": [obj.json() for obj in list(Stage.objects.filter(project=project_id).all())]}
    if stage:
        return JsonResponse(stage)
    else:
        return JsonResponse({'stage': []})
