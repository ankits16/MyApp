from django.db import models
from core.abstract.models import AbstractManager, AbstractModel
# Create your models here.

class PostManager(AbstractManager):
    pass

class Post(AbstractModel):
    author = models.ForeignKey(to="core_user.User", on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self) -> str:
        return f"{self.author.name} ({self.body})"
    
    class Meta:
        db_table = "'core.post'"

