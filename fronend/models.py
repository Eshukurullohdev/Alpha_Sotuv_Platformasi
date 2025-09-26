from django.db import models

class Product(models.Model):
    PRODUCT_TYPES = (
        ('simple', 'Simple'),
        ('premium', 'Premium'),
    )

    name = models.CharField(max_length=200, verbose_name="Nomi")
    img = models.ImageField(upload_to='media/', blank=True, null=True, verbose_name="Rasm")
    narx = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='simple', verbose_name="Turi")
    tavsif = models.TextField(verbose_name="Tavsifi")

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
