# Generated by Django 4.1.5 on 2023-02-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0010_alter_project_html_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='labels',
            field=models.ManyToManyField(to='contributors.contributionlabel', verbose_name='contribution labels'),
        ),
    ]
