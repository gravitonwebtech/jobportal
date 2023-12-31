# Generated by Django 3.0.14 on 2022-05-27 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_newsletter_phone'),
        ('jobsapp', '0004_doucmentemp_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoucmentEmpMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyIdCard', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('shopStablished', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('udyogAAdhar', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('certificateOfIncorpation', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('msmacertificate', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('Tan', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('Din', models.FileField(blank=True, null=True, upload_to='uploads/category')),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.DeleteModel(
            name='DoucmentEmp',
        ),
    ]
