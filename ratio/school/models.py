from django.contrib.auth.models import User
from django.db import models


class Activation(models.Model):
    """Represents an User that hasn't verified the
    email yet."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The connected User object"""

    created_at = models.DateTimeField(auto_now_add=True)
    """When the Activation object has been created"""

    code = models.CharField(max_length=20, unique=True)
    """The activation code"""

    email = models.EmailField(blank=True)
    """The user email"""
