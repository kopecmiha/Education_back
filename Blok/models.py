from django.db import models
import json, time


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    last_name = models.TextField()
    patronimyc = models.TextField(default="")
    type = models.TextField(default="")
    email = models.TextField()
    password = models.TextField()
    organization = models.TextField(default="")
    position = models.TextField(default="")
    contacts = models.TextField(default="")
    avatar_image = models.FileField(upload_to="avatars", null=True)

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "last_name": self.last_name,
                "patronimyc": self.patronimyc,
                "type": self.type,
                "email": self.email,
                "password": self.password,
                "organization": self.organization,
                "position": self.position,
                "contacts": self.contacts,
                "avatar_image": self.avatar_image.name
                }


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    def create(self, id, name):
        self.name = name
        self.save()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Recrut(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    def create(self, id, name, ):
        self.name = name
        self.save()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default=None)
    description = models.TextField()
    image = models.FileField(upload_to="project_images", null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)
    recruts = models.ManyToManyField(Recrut)
    category = models.TextField(default="")

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "image": self.image.name,
                "creator": self.creator.json(),
                "tags": [obj.json() for obj in list(self.tags.all())],
                "recruts": [obj.json() for obj in list(self.recruts.all())],
                "category": self.category
                }


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField()

    def json(self):
        return {"user": self.user.json(),
                "project": self.project.json(),
                "name": self.name,
                }


class Comment(models.Model):
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def json(self):
        return {
            "description": self.description,
            "date": self.date,
            "project": self.project.json(),
            "user": self.user.json(),
            "id": self.id
        }


class Event(models.Model):
    name = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def json(self):
        return {
            "name": self.name,
            "date": self.date,
            "project": self.project.json(),
            "user": self.user.json(),
            "id": self.id
        }


class Column(models.Model):
    order = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField()

    def json(self):
        return {
            "name": self.name,
            "order": self.order,
            "project": self.project.json(),
        }


class Card(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    order = models.IntegerField()
    date_start = models.IntegerField(default=0)
    date_finish = models.IntegerField(default=0)

    def json(self):
        return {
            "column": self.column.json(),
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "date_start": self.date_start,
            "date_finish": self.date_finish
        }


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    file = models.TextField()
    date = models.IntegerField(default=0)
    type = models.TextField(default="")
    link = models.TextField(default="")

    def json(self):
        return {"id": self.id,
                "user": self.user.json(),
                "project": self.project.json(),
                "name": self.name,
                "description": self.description,
                "file": self.file,
                "date": self.date,
                "type": self.type,
                "link": self.link
                }


class ActivityComment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    activity = models.TextField()
    date = models.IntegerField()
    user = models.TextField()

    def json(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": self.date,
            "activity": self.activity,
            "user": User.objects.filter(id=self.user).first().json(),
        }


class Stage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    project = models.TextField()
    date = models.IntegerField()
    period = models.TextField()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "project": self.project,
            "period": self.period,
        }


class Money(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.IntegerField()
    sum = models.IntegerField()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "stage": self.stage.json(),
            "user": self.user.json(),
            "date": self.date,
            "sum": self.sum,
        }
