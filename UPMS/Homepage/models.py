from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Departments(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Departments'
        verbose_name_plural = 'Departments'


class Course(models.Model):
    name = models.CharField(max_length=256)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Courses'
        verbose_name_plural = 'Courses'


class Companies(models.Model):
    name = models.CharField(max_length=256)
    about = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Companies'
        verbose_name_plural = 'Companies'


class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True)
    GENDER = (
        (1,'Male'),
        (2,'Female'),
        (3,'Other')
    )
    
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    dob = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True, unique=True)
    whatsapp = models.CharField(max_length = 20, null=True, blank=True, unique=True)
    
    address = models.TextField(help_text = "Enter address")
    city = models.CharField(max_length=50, help_text = "Enter City")
    pincode = models.CharField(max_length=6, help_text = "Enter pincode")
    state = models.CharField(max_length=50, help_text = "Enter state")

    ssc = models.CharField(max_length=128, null=True, blank=True)
    ssc_year = models.PositiveSmallIntegerField(null=True, blank=True)
    ssc_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    ssc_cgpa = models.FloatField(null=True, blank=True)

    hssc = models.CharField(max_length=128, null=True, blank=True)
    hssc_year = models.PositiveSmallIntegerField(null=True, blank=True)
    hssc_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    hssc_cgpa = models.FloatField(null=True, blank=True)

    ug = models.CharField(max_length=128, null=True, blank=True)
    ug_year = models.PositiveSmallIntegerField(null=True, blank=True)
    ug_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    ug_cgpa = models.FloatField(null=True, blank=True)

    pg = models.CharField(max_length=128, null=True, blank=True)
    pg_year = models.PositiveSmallIntegerField(null=True, blank=True)
    pg_percentage = models.PositiveSmallIntegerField(null=True, blank=True)
    pg_cgpa = models.FloatField(null=True, blank=True)


    department_name = models.ForeignKey(Departments, blank=True, null=True, on_delete=models.CASCADE, related_name='department_name')
    course_name = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    placed_in = models.ManyToManyField(Companies, blank=True, related_name='placed_in')
    salary = models.FloatField(null=True, blank=True)
    
    is_student = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_placed = models.BooleanField(default=False)


    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='last login', default=timezone.now)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.username)
    
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'


class Drives(models.Model):
    name = models.CharField(max_length=256, help_text = "Drive name")
    DRIVE_TYPE = (
        (1,'Virtual'),
        (2,'On Campus'),
        (3,'Off Campus')
    )
    drive_type = models.PositiveSmallIntegerField(choices=DRIVE_TYPE, help_text ="Enter type of drive")
    created = models.DateTimeField(default = timezone.now)
    drive_on = models.DateField(help_text="Enter in the following format : YYYY-MM-DD")
    STREAMS = (
        (1,'MCA'),
        (2,'BCA'),
        (3,'B Tech')
    )
    stream_required = models.PositiveSmallIntegerField(choices=STREAMS)
    batch_year = models.IntegerField(('year'), default=datetime.now().year)
    eligibility = models.IntegerField(blank=True)
    position = models.CharField(max_length=255, blank=True)
    job_profile = models.CharField(max_length=255, blank=True)
    JOB_TYPE_CHOICE = (
        (1,'WFH'),
        (2,'Full Time'),
        (3,'Internship')
    )
    job_type = models.PositiveSmallIntegerField(choices=JOB_TYPE_CHOICE)
    job_location = models.CharField(max_length=255, blank=True)
    date_of_joining = models.DateField()
    stipend_package = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Drives'
        verbose_name_plural = 'Drives'


class Responses(models.Model):
    drive = models.ForeignKey(Drives, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_TITLE = (
        (1,'Applied'),
        (2,'Processing'),
        (3,'Shortlisted'),
        (4,'Rejected'),
        (5,'Selected')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_TITLE, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s-%s' % (self.user.username, self.drive.name)

    class Meta:
        verbose_name = 'Responses'
        verbose_name_plural = 'Responses'


class Announcements(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcements'
        verbose_name_plural = 'Announcements'