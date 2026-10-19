from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="CarMake",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(choices=[
                    ("Sedan", "Sedan"), ("SUV", "SUV"), ("Wagon", "Wagon"),
                    ("Coupe", "Coupe"), ("Convertible", "Convertible"),
                    ("Hatchback", "Hatchback"), ("Truck", "Truck"),
                ], max_length=30)),
                ("year", models.PositiveIntegerField(validators=[
                    django.core.validators.MinValueValidator(2015),
                    django.core.validators.MaxValueValidator(2023),
                ])),
                ("make", models.ForeignKey(
                    on_delete=models.deletion.CASCADE, related_name="models", to="djangoapp.carmake"
                )),
            ],
            options={"unique_together": {("make", "name", "year")}},
        ),
    ]
