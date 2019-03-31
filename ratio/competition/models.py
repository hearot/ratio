from typing import Dict, List

import tinymce.models
from django.contrib.auth.models import User
from django.db import models


class Answer(models.Model):
    """Represents an Answer given by a Contestant
    during a Competition"""

    participant = models.ForeignKey('Contestant', on_delete=models.CASCADE)
    """The Contestant who has given the answer"""

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

    def get_leaderboard(self) -> Dict[str, List[int]]:
        """Returns a dictionary where the key is
        an username and the value is a list with all
        the points got by the user."""
        return {contestant.user.username: contestant.get_list_points() for contestant in
                self.contestants.filter(race=self)}


class Contestant(models.Model):
    """Represents an User that has joined the Competition."""

    answers = models.ManyToManyField('Answer', blank=True, default=[])
    """All the Answers given by the Contestant."""

    race = models.ForeignKey('Competition', on_delete=models.CASCADE)
    """The associated Competition."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The associated user."""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.user)

    def get_list_points(self) -> List[int]:
        """Returns a list with all the points got from
        Questions."""
        return [self.get_question_points(question) for question in Question.objects.filter(race=self.race)]

    def get_question_points(self, question: 'Question') -> int:
        """Returns all the points got from a Question."""
        try:
            return sum(*[answer.point for answer in self.answers.filter(question=question, participant=self)])
        except TypeError:
            return 0

    def get_total_points(self) -> int:
        """Return the total points."""
        try:
            return sum(*self.get_list_points())
        except TypeError:
            return 0


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
