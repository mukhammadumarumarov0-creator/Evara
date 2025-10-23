from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

choice=(
   
   ("Pending","Pending"),
   ("Accepted", "Accepted"),
   ("Canceled","Canceled")
)

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
   
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    items=models.ManyToManyField(OrderItem)
    address=models.CharField(max_length=200,blank=True,null=True)
    additional=models.CharField(max_length=200,blank=True,null=True)
    status=models.CharField(max_length=20,null=True,choices=choice,default="Pending")

    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"Bu orderni {self.user.username}"
    
    def get_total(self):
       total_price=0
       for i in self.items.all():
          total_price += i.total_price
      
       return total_price
          

