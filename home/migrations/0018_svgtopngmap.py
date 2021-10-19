# Generated by Django 3.1.13 on 2021-10-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_merge_20211004_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='SVGToPNGMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('svg_path', models.TextField()),
                ('fill_color', models.TextField(null=True)),
                ('stroke_color', models.TextField(null=True)),
                ('png_image_file', models.ImageField(upload_to='svg-to-png-maps/')),
            ],
            options={
                'unique_together': {('svg_path', 'fill_color', 'stroke_color')},
            },
        ),
    ]
