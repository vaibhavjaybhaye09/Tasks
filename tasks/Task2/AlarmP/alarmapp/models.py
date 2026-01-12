from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=50, unique=True)
    current_value = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Threshold(models.Model):
    STATUS_CHOICES = (
        ('RIGHT', 'Right'),
        ('WRONG', 'Wrong'),
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='thresholds'
    )
    limit_value = models.IntegerField()
    status_type = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:
        ordering = ['limit_value']

    def __str__(self):
        return f"{self.station.name} - {self.status_type} ({self.limit_value})"
