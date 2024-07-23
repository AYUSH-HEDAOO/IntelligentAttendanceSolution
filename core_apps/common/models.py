import uuid
from django.db import models

# This model is abstract model which will be inherit by other models accross all the core apps
class IASModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) # Soft delete

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]