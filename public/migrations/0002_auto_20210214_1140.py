# Generated by Django 2.1.15 on 2021-02-14 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='actualitem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='superuser.Item'),
        ),
        migrations.AlterField(
            model_name='cartitemdetail',
            name='Category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='superuser.Categories'),
        ),
    ]