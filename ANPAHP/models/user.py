from django.db import models

class User(models.Model):
    """Model representing a user in our DB."""
    first_name = models.CharField('First Name', max_length = 120)
    last_name = models.CharField('Last Name', max_length = 120)
    email_address = models.EmailField('User Email', unique = True)

    def __str__(self): 
        """Overrides the str() methods. Used for a human readable form of the model."""
        return f"{self.first_name} {self.last_name} ({self.email_address})"