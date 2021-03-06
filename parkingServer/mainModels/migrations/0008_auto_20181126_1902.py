# Generated by Django 2.1.2 on 2018-11-26 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainModels', '0007_auto_20181125_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='camId',
        ),
        migrations.AddField(
            model_name='camera',
            name='cameraID',
            field=models.CharField(default='1.1', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='camera',
            name='sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camera', to='mainModels.Sector'),
        ),
    ]
