from django.db import models

class CategoryChoices(models.IntegerChoices):
    CLIENT = 1, 'Client'
    STAFF_MEMBER = 2, 'Staff Member'
    GENERAL_USER = 6, 'General User'

class SubCategoryChoices(models.IntegerChoices):
    NO_SELECTION = 0, 'No selection'
    FULL_TIME = 1, 'Full Time'
    CONTRACTUAL = 2, 'Contractual'
    AGENT = 3, 'Agent'
    SHORT_TERM = 4, 'Short Term'
    LONG_TERM = 5, 'Long Term'
    CURRENT = 6, 'Current'
    PROSPECTIVE = 7, 'Prospective'
    OTHER = 8, 'Other'