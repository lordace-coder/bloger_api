# Generated by Django 4.2.4 on 2023-10-29 05:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0015_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True
            ),
        ),
    ]
