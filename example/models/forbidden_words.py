from django.db import models

class swear_words(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word