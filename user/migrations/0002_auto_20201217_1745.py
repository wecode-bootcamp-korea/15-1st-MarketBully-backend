# Generated by Django 3.1.4 on 2020-12-17 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(max_length=45, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=45, unique=True),
        ),
        migrations.CreateModel(
            name='OftenBuying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'often_buyings',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='often_buying',
            field=models.ManyToManyField(related_name='often_buying_set', through='user.OftenBuying', to='product.Product'),
        ),
    ]