from django.db import models
from shop.models import Product


class Review(models.Model):
    comment_text=models.TextField()
    username=models.CharField(max_length=200)
    email=models.EmailField(null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}'s comment"

