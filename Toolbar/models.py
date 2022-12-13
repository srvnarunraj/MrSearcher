from django.db import models

class SearchText(models.Model):
    SearchText = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.SearchText