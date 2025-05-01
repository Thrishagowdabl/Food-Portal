# portal/migrations/0003_donor_delete_profile.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_profile'),  # Ensure this is the previous migration
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),  # Only include fields you want
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='portal.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',  # Make sure to remove Profile model if no longer needed
        ),
    ]
