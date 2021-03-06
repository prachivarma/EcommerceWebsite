# Generated by Django 3.0.8 on 2020-10-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='carousel_img')),
            ],
            options={
                'db_table': 'tbl_carousel_images',
            },
        ),
    ]
