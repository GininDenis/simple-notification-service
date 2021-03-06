# Generated by Django 2.1.4 on 2019-01-16 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20181227_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='attempts_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Attempts count'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='error_msg',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Error message'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='notifications.Topic', verbose_name='Topic'),
        ),
    ]
