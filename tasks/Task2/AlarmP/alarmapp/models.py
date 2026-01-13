from django.db import models
from django.core.validators import MinValueValidator


class Station(models.Model):
    name = models.CharField(max_length=50, unique=True)
    current_value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Threshold(models.Model):
    station = models.OneToOneField(
        Station,
        on_delete=models.CASCADE,
        related_name='threshold'
    )
    limit_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.station.name} → Limit {self.limit_value}"
    class Meta:
        unique_together = ('station', 'limit_value')