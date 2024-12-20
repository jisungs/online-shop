# Generated by Django 5.1.1 on 2024-10-14 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_order_id', models.CharField(blank=True, max_length=120, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=120, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('transaction_status', models.CharField(blank=True, max_length=220, null=True)),
                ('type', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
