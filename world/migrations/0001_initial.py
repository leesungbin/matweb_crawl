# Generated by Django 2.1.7 on 2019-05-25 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compound', models.CharField(default='', max_length=256)),
                ('ratio', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Stainless',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('num', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('stainless', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Stainless')),
            ],
        ),
        migrations.CreateModel(
            name='TensileStrength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.FloatField(blank=True, null=True)),
                ('crit', models.FloatField(blank=True, default=20, null=True)),
                ('cond', models.CharField(blank=True, max_length=256, null=True)),
                ('stainless', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Stainless')),
            ],
        ),
        migrations.CreateModel(
            name='ThermodynamicProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k', models.FloatField(blank=True, default=0, null=True)),
                ('crit', models.FloatField(blank=True, default=20, null=True)),
                ('stainless', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Stainless')),
            ],
        ),
        migrations.CreateModel(
            name='YieldStrength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.FloatField(blank=True)),
                ('crit', models.FloatField(blank=True, default=20, null=True)),
                ('cond', models.CharField(blank=True, max_length=256, null=True)),
                ('stainless', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Stainless')),
            ],
        ),
        migrations.AddField(
            model_name='composition',
            name='stainless',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Stainless'),
        ),
    ]