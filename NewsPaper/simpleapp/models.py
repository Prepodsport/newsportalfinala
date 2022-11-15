from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(verbose_name=("Название"),
                            max_length=50,
                            unique=True,  # названия товаров не должны повторяться
                            )
    description = models.TextField(verbose_name=("Описание"), )
    quantity = models.IntegerField(verbose_name=("Количество"),
                                   validators=[MinValueValidator(0)],
                                   )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(verbose_name=("Категория"),
                                 to='Category',
                                 on_delete=models.CASCADE,
                                 related_name='products',  # все продукты в категории будут доступны через поле products
                                 )
    price = models.FloatField(verbose_name=("Цена"),
                              validators=[MinValueValidator(0.0)],
                              )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:
        verbose_name = ("Продукт")
        verbose_name_plural = ("Продукты")


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True, verbose_name='Категории')

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")
