from django.db import models


class EventStatus(models.TextChoices):
    NEGOTIATING = "NEGOTIATING"
    SCHEDULED = "SCHEDULED"
    DONE = "DONE"
    CHOOSING = "CHOOSING"
    EDITING = "EDITING"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"
