from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="category_images/",null=True,blank=True)


    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.PositiveIntegerField(default=0)
    discount_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    description=models.TextField()
    quantity=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="products/",null=True,blank=True)

    def save(self,*args, **kwargs):

        if self.discount>0:
            self.discount_price=self.price-self.price*self.discount/100

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
   

    