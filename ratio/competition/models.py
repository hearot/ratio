from typing import Dict, List

import tinymce.models
from django.contrib.auth.models import User
from django.db import models


class Answer(models.Model):
    """Represents an Answer given by a Contestant
    during a Competition"""

    contestant = models.ForeignKey('Contestant', on_delete=models.CASCADE)
    """The Contestant who has given the answer"""

    point = models.IntegerField()
    """How many points have been added/subtracted."""

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    """The associated question"""

    right = models.BooleanField()
    """If the given Answer is right"""

    unique_together = ("contestant", "question", "right")

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str("%s (±%s)" % (self.question, self.point))


class Competition(models.Model):
    """Represents a Competition where Contestants have
    to give Answers about some Questions."""

    description = tinymce.models.HTMLField()
    """The Question text - the description"""

    end = models.DateTimeField()
    """When the Competition ends"""

    start = models.DateTimeField()
    """When the Competition starts"""

    tag = models.CharField(max_length=50)
    """The tag used in the Competitions index"""

    title = models.CharField(max_length=20)
    """The title of the question"""

    unique_together = ("title", "start", "end")

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return "%s" % self.title

    def get_contestants(self) -> List['Contestant']:
        """Returns a list of all the Contestants that
        joined the Competition."""
        return Contestant.objects.filter(competition=self)

    def get_leaderboard(self) -> Dict[str, List[int]]:
        """Returns a dictionary where the key is
        an username and the value is a list with all
        the points got by the user."""
        return {contestant.user.username: contestant.get_list_points() for contestant in
                self.get_contestants()}

    def get_questions(self) -> List['Question']:
        """Returns a list of all the Questions that
        are proposed during the Competition."""
        return Question.objects.filter(competition=self)


class Contestant(models.Model):
    """Represents an User that has joined the Competition."""

    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)
    """The associated Competition."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The associated user."""

    unique_together = ("competition", "user")

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.user)

    def get_answer_by_question(self, question: 'Question') -> List[Answer]:
        """Returns a list with all the Answers given
        by the Contestant."""
        return Answer.objects.filter(contestant=self, question=question)

    def get_answers(self) -> List[Answer]:
        """Returns a list with all the Answers given
        by the Contestant."""
        return Answer.objects.filter(contestant=self)

    def get_list_points(self) -> List[int]:
        """Returns a list with all the points got from
        Questions."""
        return [self.get_question_points(question) for question in
                Question.objects.filter(competition=self.competition)]

    def get_question_points(self, question: 'Question') -> int:
        """Returns all the points got from a Question."""
        try:
            return sum(*[answer.point for answer in self.get_answer_by_question(question)])
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

    competition = models.ForeignKey('Competition', blank=False, on_delete=models.CASCADE)
    """To which Competition the Question is associated"""

    description = tinymce.models.HTMLField()
    """The Question text - the description"""

    explanation = tinymce.models.HTMLField()
    """The explanation of the solution"""

    point = models.IntegerField(default=100)
    """How many points are given if the answer is correct"""

    right_answer = models.CharField(max_length=25)
    """The right answer to the question"""

    title = models.CharField(max_length=35)
    """The title of the question"""

    unique_together = ("title", "competition")

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.title)