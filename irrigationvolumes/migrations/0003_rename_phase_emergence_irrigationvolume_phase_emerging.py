# Generated by Django 5.1.7 on 2025-04-06 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irrigationvolumes', '0002_alter_irrigationvolume_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='irrigationvolume',
            old_name='phase_emergence',
            new_name='phase_emerging',
        ),
    ]
