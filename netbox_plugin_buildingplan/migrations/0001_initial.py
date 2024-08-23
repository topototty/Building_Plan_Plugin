from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenancy', '0015_contactassignment_rename_content_type'),  # Укажите правильную миграцию
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='building_plans/')),
                ('tenant', models.OneToOneField(on_delete=models.CASCADE, related_name='building_plan', to='tenancy.Tenant')),
            ],
        ),
    ]
