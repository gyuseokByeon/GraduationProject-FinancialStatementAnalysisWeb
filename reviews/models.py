from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse
from django.db import models
from . import managers

#리뷰
class Review(models.Model):

    #기업
    corp = models.ForeignKey(
        "corps.Corp", related_name="reviews", on_delete=models.CASCADE
    )

    #작성자
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )

    #리뷰 내용
    comment = models.TextField()

    #평점
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    #작성일
    created = models.DateTimeField(auto_now_add=True)
