from django.db import models

class SearchText(models.Model):
    Searchtext = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.Searchtext