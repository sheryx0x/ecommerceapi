from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price =  models.DecimalField(max_digits=8 , decimal_places=2)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    customer_name = models.CharField(max_length = 100) 
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name= 'items')
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()