# Generated by Django 4.1.4 on 2023-03-11 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_post_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='likes',
            new_name='numLikes',
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('chirpId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.post')),
            ],
        ),
    ]
