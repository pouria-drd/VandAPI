# Generated by Django 5.1 on 2024-09-02 09:09

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RemoveIndex(
            model_name='product',
            name='shop_produc_name_a2070e_idx',
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name', 'slug', 'is_active'], name='shop_produc_name_731dfe_idx'),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='shop.product'),
        ),
        migrations.AddIndex(
            model_name='price',
            index=models.Index(fields=['amount', 'is_active', 'created_at'], name='shop_price_amount_91b116_idx'),
        ),
    ]