# Generated by Django 4.0.4 on 2022-06-02 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('idr', models.AutoField(db_column='IdR', primary_key=True, serialize=False)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=1, null=True)),
                ('idc', models.ForeignKey(blank=True, db_column='IdC', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cars.car')),
                ('idu', models.ForeignKey(blank=True, db_column='IdU', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.user')),
            ],
            options={
                'db_table': 'reservation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ratingdriver',
            fields=[
                ('ido', models.AutoField(db_column='IdO', primary_key=True, serialize=False)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('descr', models.CharField(blank=True, max_length=500, null=True)),
                ('idd', models.ForeignKey(blank=True, db_column='IdD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='IdD', to='users.user')),
                ('idr', models.ForeignKey(blank=True, db_column='IdR', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='reservations.reservation')),
                ('idu', models.ForeignKey(blank=True, db_column='IdU', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='IdU', to='users.user')),
            ],
            options={
                'db_table': 'ratingdriver',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ratingcar',
            fields=[
                ('ido', models.AutoField(db_column='IdO', primary_key=True, serialize=False)),
                ('car_rating', models.IntegerField(blank=True, null=True)),
                ('descr', models.CharField(blank=True, max_length=500, null=True)),
                ('djiler_rating', models.IntegerField(blank=True, null=True)),
                ('idc', models.ForeignKey(blank=True, db_column='IdC', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cars.car')),
                ('idd', models.ForeignKey(blank=True, db_column='IdD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.user')),
                ('idr', models.ForeignKey(blank=True, db_column='IdR', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='reservations.reservation')),
            ],
            options={
                'db_table': 'ratingcar',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('idr', models.OneToOneField(db_column='IdR', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='reservations.reservation')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('idc', models.ForeignKey(db_column='IdC', on_delete=django.db.models.deletion.DO_NOTHING, to='cars.car')),
            ],
            options={
                'db_table': 'holding',
                'managed': True,
            },
        ),
    ]
