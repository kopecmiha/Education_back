from django.db import models
import json

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
    def create(self, id, name, description, image, creator):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.creator = creator
        self.save()

    def json(self):
        return {"id": self.id,
                    "name": self.name,
                    "description": self.description,
                    "image": self.image,
                    "creator": [obj.json() for obj in list(self.creator.all())],
                    "tags": [obj.json() for obj in list(self.tags.all())],
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