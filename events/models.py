from django.db import models


class Event(models.Model):
    class Specialties(models.TextChoices):
        ORTHO = "Orthopedics"
        FAMILY = "Family"

    date = models.DateField()
    specialty = models.CharField(
        max_length=11,
        choices=Specialties.choices,
        default=Specialties.FAMILY,
    )
    description = models.CharField(max_length=100)

    class Meta:
        app_label = "events"

    def __str__(self):
        return (
            f"ID: {self.id}, Date {self.date}, Speciality {self.specialty}, "
            f"Description {self.description}"
        )
