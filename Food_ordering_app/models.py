from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    pizza_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(upload_to="images/")
    
    def __str__(self):
       return self.pizza_name
    
    
class PizzaTopping(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='carts') 

    def __str__(self):
        return self.user.username
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='cart_items' )
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)

    
    def __str__(self):
        return f"{self.quantity} x {self.menuitem.pizza_name}"
    

class Order(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='orders')
    time = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    in_cart = models.BooleanField(default=True)
    placed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    category = models.CharField(max_length=20)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings = models.ManyToManyField(PizzaTopping, blank=True, related_name='order_items')
    

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.pizza_name}" 
    

class ShippingInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.full_name
