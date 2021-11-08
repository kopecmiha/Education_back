from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default=None)
    last_name = models.TextField()
    patronimyc = models.TextField()
    type = models.TextField()
    email = models.TextField()
    password = models.TextField()
    organization = models.TextField()
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
                    "password": self.password,
                    "organization": self.organization,
                    "avatar_image": self.avatar_image
                    })
