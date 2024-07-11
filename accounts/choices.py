from django.db import models

class CategoryChoices(models.IntegerChoices):
    Job_Applicant = 1
    Coda_Staff_Member = 2
    Jobsupport = 3
    Student = 4 
    investor = 5
    Vendor=6
    General_User = 7

    
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