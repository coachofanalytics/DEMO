from django.db import models

class CategoryChoices(models.IntegerChoices):
    Bussines_Training = 1
    Jobsupport = 2
    investor = 4
    General_User = 5

    
class SubCategoryChoices(models.IntegerChoices):
    No_selection = 0
    #Staff category
    Full_time = 1
    Contractual = 2
    Agent = 3
    #investors category
    Short_Term = 4
    Long_Term = 5
    #students/Job Support
    current = 6
    prospective = 7

    Other = 8