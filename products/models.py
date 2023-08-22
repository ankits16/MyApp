from django.db import models
from core.abstract.models import AbstractManager, AbstractModel

# Create your models here.
class ProductManager(AbstractManager):
    pass
class Product(AbstractModel):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    objects = ProductManager()

    def __str__(self) -> str:
        return f"{self.title} ({self.image})"