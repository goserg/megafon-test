from django.db import models

# Create your models here.
class Money(models.Model):
  value = models.DecimalField(max_digits=12, decimal_places=2)
  hasNds = models.BooleanField(default=False)
  nds = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
  parsed = models.TextField(blank=True, null=True)


  def __str__(self):
    return f"{self.value}{(', +' + str(self.nds) + '% НДС') if self.nds else ', без НДС'}"