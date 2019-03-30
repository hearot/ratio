from django.contrib.auth.models import User
from django.db import models

import tinymce.models


class Answer(models.Model):
    """Represents an Answer given by a Contestant
    during a Competition"""

    point = models.IntegerField()
    """How many points have been added/subtracted."""

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    """The associated question"""

    right = models.BooleanField()
    """If the given Answer is right"""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str("%s (±%s)" % (self.question, self.point))


class Competition(models.Model):
    """Represents a Competition where Contestants have
    to give Answers about some Questions."""

    contestants = models.ManyToManyField('Contestant', blank=True)
    """All the Contestants that have joined the competition"""

    description = tinymce.models.HTMLField()
    """The Question text - the description"""

    end = models.DateTimeField()
    """When the Competition ends"""

    questions = models.ManyToManyField('Question')
    """All the Questions proposed in the competition"""

    start = models.DateTimeField()
    """When the Competition starts"""

    title = models.CharField(max_length=20)
    """The title of the question"""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return "%s" % self.title


class Contestant(models.Model):
    """Represents an User that has joined the Competition."""

    answers = models.ManyToManyField('Answer', blank=True, default=[])
    """All the Answers given by the Contestant."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The associated user."""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.user)


class Question(models.Model):
    """Represents a Question that could be given
    in a Competition."""

    race = models.ForeignKey('Competition', blank=False, on_delete=models.CASCADE)
    """To which Competition the Question is associated"""

    description = tinymce.models.HTMLField()
    """The Question text - the description"""

    point = models.IntegerField(default=100)
    """How many points are given if the answer is correct"""

    right_answer = models.CharField(max_length=10)
    """The right answer to the question"""

    title = models.CharField(max_length=20)
    """The title of the question"""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.title)
