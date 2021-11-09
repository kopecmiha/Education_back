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
    avatar_image = models.TextField()

    def create(self, id, name, last_name, patronimyc, type, email, password, organization, avatar_image):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.patronimyc = patronimyc
        self.type = type
        self.email = email
        self.password = password
        self.organization = organization
        self.avatar_image = avatar_image
        self.save()

    def __str__(self):
        return str({"id": self.id,
                    "name": self.name,
                    "last_name": self.last_name,
                    "patronimyc": self.patronimyc,
                    "type": self.type,
                    "email": self.email,
                    "password": self.password,
                    "organization": self.organization,
                    "avatar_image": self.avatar_image
                    })
    def json(self):
        return {"id": self.id,
                    "name": self.name,
                    "last_name": self.last_name,
                    "patronimyc": self.patronimyc,
                    "type": self.type,
                    "email": self.email,
                    "password": self.password,
                    "organization": self.organization,
                    "avatar_image": self.avatar_image
                    }


class Tag(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField()

    def create(self, id, name, project):
        self.name = name
        self.save()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            }


class Project(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(default=None)
    description = models.TextField()
    image = models.TextField()
    creator = models.ManyToManyField(User)
    tags = models.ManyToManyField(Tag)
    category = models.TextField(default="")
    def create(self, id, name, description, image, creator, category):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.creator = creator
        self.category = category
        self.save()

    def json(self):
        return {"id": self.id,
                    "name": self.name,
                    "description": self.description,
                    "image": self.image,
                    "creator": [obj.json() for obj in list(self.creator.all())],
                    "tags": [obj.json() for obj in list(self.tags.all())],
                    "category": self.category
                    }
#name, description, image, creator


class Status(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    name = models.TextField()

    def create(self, user, project, name):
        self.user = user
        self.project = project
        self.name = name
        self.save()

    def json(self):
        return {"user": self.user.json(),
                    "project": self.project.json(),
                    "name": self.name,
                    }




class Comment(models.Model):
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    date = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)


    def create(self, description, project, date, user):
        self.description = description
        self.project = project
        self.date = date
        self.user = user
        self.save()

    def json(self):
        return {
            "description": self.description,
            "date": self.date,
            "project": self.project.json(),
            "user": self.user.json(),
        }

class Event(models.Model):
    name = models.TextField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    date = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)


    def create(self, name, project, date, user):
        self.name = name
        self.project = project
        self.date = date
        self.user = user
        self.save()

    def json(self):
        return {
            "name": self.name,
            "date": self.date,
            "project": self.project.json(),
            "user": self.user.json(),
        }

class Column(models.Model):
    order = models.IntegerField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    name = models.TextField()


    def create(self, name, project, order):
        self.name = name
        self.project = project
        self.order = order
        self.save()

    def json(self):
        return {
            "name": self.name,
            "order": self.order,
            "project": self.project.json()
        }


class Card(models.Model):
    column = models.ForeignKey(Column,  on_delete = models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    order = models.IntegerField()


    def create(self, column, name, description, order):
        self.column = column
        self.name = name
        self.description = description
        self.order = order
        self.save()

    def json(self):
        return {
            "column": self.column.json(),
            "name": self.name,
            "description": self.description,
            "order": self.order,
        }

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    file = models.TextField()
    date = models.IntegerField(default = 0)
    type = models.TextField(default = "")

    def create(self, user, project, name, description, file, date, id, type):
        self.id = id
        self.user = user
        self.project = project
        self.name = name
        self.description = description
        self.file = file
        self.date = date
        self.type = type
        self.save()

    def json(self):
        return {"id": self.id,
                "user": self.user.json(),
                "project": self.project.json(),
                "name": self.name,
                "description": self.description,
                "file": self.file,
                "date": self.date,
                "type": self.type
                }

class ActivityComment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    activity = models.TextField()
    date = models.IntegerField()
    user = models.TextField()


    def create(self, id, description, activity, date, user):
        self.id = id
        self.description = description
        self.activity = activity
        self.date = date
        self.user = user
        self.save()

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


    def create(self, id, name, description, project, date, period):
        self.id = id
        self.name = name
        self.description = description
        self.project = project
        self.date = date
        self.period = period
        self.save()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "project": self.project,
            "period": self.period,
        }