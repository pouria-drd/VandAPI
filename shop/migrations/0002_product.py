# Generated by Django 5.1 on 2024-09-02 09:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='slug')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='shop.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['name'], name='shop_produc_name_a2070e_idx')],
            },
        ),
    ]
