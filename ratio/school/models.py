# Ratio: Quisque faber fortunae suae.
# Copyright (C) 2019 Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
