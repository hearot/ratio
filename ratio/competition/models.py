from typing import Dict, List

import tinymce.models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Answer(models.Model):
    """Represents an Answer given by a Contestant
    during a Competition"""

    contestant = models.ForeignKey('Contestant', on_delete=models.CASCADE)
    """The Contestant who has given the answer"""

    given_answer = models.CharField(max_length=25)
    """The answer given by the Contestant."""

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

    can_join_when_started = models.BooleanField(default=False)
    """If an User can join the Competition even if
    this has already begun."""

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
        leaderboard = {contestant.user.username: contestant.get_list_points() for contestant in
                       self.get_contestants()}

        return {key: leaderboard[key] for key in sorted(leaderboard,
                                                        key=lambda key: sum(leaderboard[key])
                                                        if leaderboard[key] else 0, reverse=True)}

    def get_questions(self) -> List['Question']:
        """Returns a list of all the Questions that
        are proposed during the Competition."""
        return Question.objects.filter(competition=self)

    def has_ended(self) -> bool:
        """If the Competition has ended."""
        return timezone.now() >= self.end

    def has_started(self) -> bool:
        """If the Competition has started."""
        return timezone.now() >= self.start

    def how_many_questions(self) -> int:
        """Returns the length of the Questions
        list."""
        return len(self.get_questions())

    def is_contestant(self, user: User) -> bool:
        """Returns if the passed User has
        joined the Competition."""
        try:
            return Contestant.objects.get(competition=self, user=user) in self.get_contestants()
        except Exception:
            return False


class Contestant(models.Model):
    """Represents an User that has joined the Competition."""

    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)
    """The associated Competition"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The associated user"""

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
        """Returns the total points."""
        try:
            return sum(*self.get_list_points())
        except TypeError:
            return 0


class Question(models.Model):
    """Represents a Question that could be given
    in a Competition."""

    competition = models.ForeignKey('Competition', blank=False, on_delete=models.CASCADE)
    """To which Competition the Question is associated"""

    delta = models.IntegerField(default=-5, validators=[MaxValueValidator(0)])
    """How many points are subtracted to the `points` attribute
    when a correct answer is given"""

    description = tinymce.models.HTMLField()
    """The Question text - the description"""

    explanation = tinymce.models.HTMLField()
    """The explanation of the solution"""

    minimum = models.IntegerField(default=65, validators=[MinValueValidator(1)])
    """The minimum points you can get if the answer is correct"""

    point = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    """How many points are given if the answer is correct"""

    right_answer = models.CharField(max_length=25)
    """The right answer to the question"""

    title = models.CharField(max_length=35)
    """The title of the question"""

    unique_together = ("title", "competition")

    wrong = models.IntegerField(default=-10, validators=[MaxValueValidator(0)])
    """How many points are given if the answer
    is wrong (must be negative"""

    def __str__(self) -> str:
        """Returns a representation of the object."""
        return str(self.title)
