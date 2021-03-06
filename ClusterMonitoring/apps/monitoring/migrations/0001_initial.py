# Generated by Django 3.0.5 on 2020-07-23 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('IP', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ServerInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField()),
                ('Architecture', models.CharField(max_length=100)),
                ('CpuName', models.CharField(max_length=200)),
                ('Cores', models.IntegerField()),
                ('RamTotal', models.IntegerField()),
                ('RamUsed', models.IntegerField()),
                ('RamPercentage', models.IntegerField()),
                ('AvgCpu1', models.FloatField(default=0)),
                ('AvgCpu5', models.FloatField(default=0)),
                ('AvgCpu15', models.FloatField(default=0)),
                ('IsHtcondor', models.BooleanField(default=False)),
                ('IsHtcondorMaster', models.BooleanField(default=False)),
                ('IsHtcondorSubmit', models.BooleanField(default=False)),
                ('IP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Server')),
            ],
        ),
    ]
