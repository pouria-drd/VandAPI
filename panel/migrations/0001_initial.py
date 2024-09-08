# Generated by Django 5.1 on 2024-09-08 06:40

import django.db.models.deletion
import panel.models.category_model
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='slug')),
                ('icon', models.ImageField(blank=True, upload_to=panel.models.category_model.category_icon_upload_to, verbose_name='icon')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['name', 'slug', 'is_active'], name='panel_categ_name_44946c_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='slug')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='panel.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='panel.product')),
            ],
            options={
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name', 'slug', 'is_active'], name='panel_produ_name_2f1087_idx'),
        ),
        migrations.AddIndex(
            model_name='price',
            index=models.Index(fields=['product', 'is_active', 'created_at'], name='panel_price_product_5a4be6_idx'),
        ),
    ]
