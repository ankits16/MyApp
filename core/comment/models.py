from django.db import models
from core.abstract.models import AbstractManager, AbstractModel
# Create your models here.

class CommentManager(AbstractManager):
    pass

class Comment(AbstractModel):
    # The on_delete=models.PROTECT parameter in the foreign key definition 
    # specifies that if the related post is deleted, 
    # the comment's foreign key will be protected, 
    # meaning Django will raise an error if you try to delete a post that has associated comments.
    post = models.ForeignKey("core_post.Post", on_delete=models.PROTECT)
    author = models.ForeignKey("core_user.User", on_delete=models.PROTECT)
    body= models.TextField()
    edited= models.BooleanField(default=False)
    objects = CommentManager()

    def __str__(self) -> str:
        return f"{self.author.name} {self.body}"
