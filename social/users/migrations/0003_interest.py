# Generated by Django 2.2b1 on 2019-05-25 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_delete_interest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.CharField(choices=[('Hollywood', 'Hollywood'), ('Bollywood', 'Bollywood'), ('Tollywood', 'Tollywood'), ('Kollywood', 'Kollywood'), ('Others', 'Others')], max_length=50)),
                ('music', models.CharField(choices=[('Classical', 'Classical'), ('Pop', 'Pop'), ('Country', 'Country'), ('Folk', 'Folk'), ('Others', 'Others')], max_length=50)),
                ('food', models.CharField(choices=[('Indian', 'Indian'), ('Chinese', 'Chinese'), ('Italian', 'Italian'), ('Continental', 'Continental'), ('Others', 'Others')], max_length=50)),
                ('sports', models.CharField(choices=[('Cricket', 'Cricket'), ('FootBall', 'FootBall'), ('Tennis', 'Tennis'), ('Kabaddi', 'Kabaddi'), ('Others', 'Others')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
