from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Responses, User, Drives, Departments, Course, Companies, Announcements

from .forms import DriveForm
# Create your views here.

class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login')) 
        
        # If user is student
        template = "home/index_student.html"
        context = {}
        departments = Departments.objects.all()
        context['departments']=departments

        students = User.objects.filter(is_student=True)
        context['students']=students

        companies = Companies.objects.all()
        context['companies']=companies

        placed_students = User.objects.filter(is_placed=True)
        context['placed_students'] = placed_students

        offers = Responses.objects.filter(status=5)
        context['offer_letters'] = offers
        
        if request.user.is_coordinator or request.user.is_superuser:
            # if user is coordinator / superuser
            template = "home/index_admin.html"
            

        announcements = Announcements.objects.order_by('-created_on')
        context['announcements']=announcements
        
        return render(request, template, context=context)


# LOGIN / REGISTRATION SYSTEM

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, "LoginRegister/login.html")

    def post(self, request):
        if request.method == "POST":
            username = request.POST["uid"].lower()
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
            else:
                context = {
                    "message": "Invalid username or password!"
                }
                template = "LoginRegister/login.html"
                return render(request, template, context)

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('homepage'))
        else:
            template="LoginRegister/register.html"
            courseList = Course.objects.all()
            context = {
                "course": courseList
            }
            return render(request, template, context=context)
    
    def post(self, request):
        if request.method == "POST":
            template = "LoginRegister/register.html"
            context={}

            # General
            username = request.POST["uid"].lower()
            firstname = request.POST["firstName"]
            lastname = request.POST["lastName"]
            dob = request.POST["dob"]
            gender = request.POST["gender"]
            course = request.POST["course"]
            password = request.POST["password"]
            confirmPassword=request.POST["confirmPassword"]

            # Contact
            mobile = request.POST["mobile"]
            whatsapp = request.POST["whatsapp"]
            email = request.POST["email"]
            address = request.POST["address"]
            city = request.POST["city"]
            pincode = request.POST["pincode"]
            state = request.POST["state"]
            
            # Education
            ssc_name = request.POST["10-board"]
            ssc_pass = request.POST["10-passing"]
            ssc_per  = request.POST["10-per"]
            ssc_cgpa = request.POST["10-cgpa"]

            if not ssc_pass:
                ssc_pass = None
            if not ssc_per:
                ssc_per = None
            if not ssc_cgpa:
                ssc_cgpa = None
            
            if not ssc_pass:
                ssc_pass = None
            if not ssc_per:
                ssc_per = None
            if not ssc_cgpa:
                ssc_cgpa = None


            hssc_name = request.POST["12-board"]
            hssc_pass = request.POST["12-passing"]
            hssc_per  = request.POST["12-per"]
            hssc_cgpa = request.POST["12-cgpa"]

            if not hssc_pass:
                hssc_pass = None
            if not hssc_per:
                hssc_per = None
            if not hssc_cgpa:
                hssc_cgpa = None

            ug_name = request.POST["ug-name"]
            ug_pass = request.POST["gra-passing"]
            ug_per  = request.POST["gra-per"]
            ug_cgpa = request.POST["gra-cgpa"]

            if not ug_pass:
                ug_pass = None
            if not ug_per:
                ug_per = None
            if not ug_cgpa:
                ug_cgpa = None

            pg_name = request.POST["pg-name"]
            pg_pass = request.POST["pg-passing"]
            pg_per  = request.POST["pg-per"]
            pg_cgpa = request.POST["pg-cgpa"]

            if not pg_pass:
                pg_pass = None
            if not pg_per:
                pg_per = None
            if not pg_cgpa:
                pg_cgpa = None

            # Validate Password:
            if password != confirmPassword:
                context['message'] = "Password did not matched!"
                return render(request, template, context=context)
            
            # Check UID 
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                context["message"]="UID already in use!"
                return render(request, template, context=context)

            # Check email
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                context["message"]="Email already in use!"
                return render(request, template, context=context)

            user = User(username=username, first_name=firstname, last_name=lastname, 
            dob=dob, gender=gender, mobile=mobile, whatsapp=whatsapp, email=email, 
            address=address, city=city, pincode=pincode, state=state, 
            ssc=ssc_name, ssc_year=ssc_pass, ssc_percentage=ssc_per, ssc_cgpa=ssc_cgpa,
            hssc=hssc_name, hssc_year=hssc_pass, hssc_percentage=hssc_per, hssc_cgpa=hssc_cgpa,
            ug=ug_name, ug_year=ug_pass, ug_percentage=ug_per, ug_cgpa=ug_cgpa,
            pg=pg_name, pg_year=pg_pass, pg_percentage=pg_per, pg_cgpa=pg_cgpa,
            is_student=True)

            user.set_password(password)
            user.save()
            user.course_name.set(course)
            user.save()
            context["message"]="User registered successfully!"

            return render(request, template, context=context)

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return HttpResponseRedirect(reverse('login'))


class GetUsers(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "home/users.html"
        listUsers = User.objects.all()
        context = {
            "users": listUsers
        }
        return render(request, template, context=context)


# Profile
class Profile(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "Profile/profile.html"
        context={}
        username=kwargs.get('id')
        
        if request.user.is_superuser:
            user=User.objects.filter(username=username).first()               
            if user:
                context['user']=user
            else:
                context['message']='NO USER FOUND!'
        else:
            if username==request.user.username:
                user=User.objects.filter(username=username).first()
                if user:
                    context['user']=user
            else:
                context['message']="YOU CANNOT VIEW OTHER'S PROFILE!"
        
        return render(request, template, context=context)


# Drives
class GetDrives(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "Drives/drives.html"
        listDrives = Drives.objects.order_by("-drive_on")
        context = {
            "drives": listDrives
        }
        return render(request, template, context=context)

class Drive(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        drive_id=kwargs.get('id')
        drive_detail = Drives.objects.get(id=drive_id)
        template = "Drives/drive.html"
        return render(request, template, context={'drive_data':drive_detail})

class UpdateDrive(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        template = "Drives/update_drive.html"
        context={}
        drive_id=kwargs.get('id')
        drive = Drives.objects.get(id=drive_id)
        
        context['drive']=drive

        return render(request, template, context=context)

class DeleteDrive(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        drive_id=kwargs.get('id')
        drive = Drives.objects.get(id=drive_id)
        drive.delete()
        
        return HttpResponseRedirect(reverse('drives'))

class NewDrive(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "Drives/new_drive.html"
        context = {}
        context['form']=DriveForm()
        return render(request, template, context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login'))


            template = "Drives/new_drive.html"
            context = {}
            
            name = request.POST['name']
            drive_type = request.POST['drive_type']
            drive_on = request.POST['drive_on']
            stream_required = request.POST['stream_required']
            batch_year = request.POST['batch_year']
            eligibility = request.POST['eligibility']
            position = request.POST['position']
            job_profile = request.POST['job_profile']
            job_type = request.POST['job_type']
            job_location = request.POST['job_location']
            date_of_joining = request.POST['date_of_joining']
            stipend_package = request.POST['package']

            if name == "":
                context["message"]="Company name cannot be blank!"
                return render(request, template, context=context)

            try:
                drive = Drives(name=name, drive_type=drive_type, drive_on=drive_on, stream_required=stream_required,
                batch_year=batch_year, eligibility=eligibility, position=position, job_profile=job_profile,
                job_type=job_type, job_location=job_location, date_of_joining=date_of_joining,
                stipend_package=stipend_package)
                drive.save()
                context["message"]="Drive added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)
            
class ApplyDrive(View):
    def get(self, request, *args, **kwargs):
        drive_id=kwargs.get('id')
        drive=Drives.objects.get(id=drive_id)

        user_exists = Responses.objects.filter(drive=drive, user=request.user).exists()
        if user_exists:
            return HttpResponseRedirect(reverse('homepage'))
        else:
            apply = Responses(drive=drive, user=request.user)
            apply.save()
        return HttpResponseRedirect(reverse('drives'))

class DriveResponses(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        template="Drives/responses.html"
        context = {}

        drive_id=kwargs.get('id')
        drive = Drives.objects.get(id=drive_id)
        
        responses = Responses.objects.filter(drive=drive).order_by('-id')
        context['responses']=responses
        context['drive']=drive

        return render(request, template, context=context)


# Coordinator
class NewCoordinator(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "LoginRegister/add_coordinator.html"
        context = {}
        departments = Departments.objects.all()
        context['departments']=departments
        return render(request, template, context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            template = "LoginRegister/add_coordinator.html"
            context={}
            departments = Departments.objects.all()
            context['departments']=departments

            username = request.POST["uid"].lower()
            firstname = request.POST["first_name"]
            lastname = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirmPassword=request.POST["confirmPassword"]

            dob = request.POST["dob"]
            gender = request.POST["gender"]
            mobile = request.POST["phone"]
            whatsapp = request.POST["whatsapp"]
            address = request.POST["address"]
            pincode = request.POST["pincode"]
            state = request.POST["state"]
            
            if username == "":
                context["message"]="Username cannot be blank!"
                return render(request, template, context=context)

            # Validate Password:
            if password != confirmPassword:
                context['message'] = "Password did not matched!"
                return render(request, template, context=context)
            
            # Check UID 
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                context["message"]="UID already in use!"
                return render(request, template, context=context)

            # Check email
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                context["message"]="Email already in use!"
                return render(request, template, context=context)

            try:
                user = User(username=username, email=email, first_name=firstname, last_name=lastname, 
                dob=dob, gender=gender, mobile=mobile, whatsapp=whatsapp, address=address, pincode=pincode, 
                state=state, is_coordinator=True)
                user.set_password(password)
                user.save()
                context["message"]="Coordinator added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)

class Coordinators(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "home/list_coordinators.html"
        listUsers = User.objects.filter(is_coordinator=True)
        context = {
            "users": listUsers
        }
        return render(request, template, context=context)


# Department
class AddDepartment(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "LoginRegister/add_department.html"
        context = {}
        return render(request, template, context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            template = "LoginRegister/add_department.html"
            context={}

            name = request.POST["name"]
            
            if name == "":
                context["message"]="Name cannot be blank!"
                return render(request, template, context=context)

            # Check department name 
            department_exists = Departments.objects.filter(name=name).exists()
            if department_exists:
                context["message"]="Department name already exists!"
                return render(request, template, context=context)

            try:
                department = Departments(name=name)
                department.save()
                context["message"]="Department added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)

class GetDepartments(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "home/list_departments.html"
        listDepartments = Departments.objects.all()
        context = {
            "departments": listDepartments
        }
        return render(request, template, context=context)


# Course
class AddCourse(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "LoginRegister/add_course.html"
        context = {}
        departments = Departments.objects.all()
        context['departments']=departments
        return render(request, template, context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            template = "LoginRegister/add_course.html"
            context={}
            departments = Departments.objects.all()
            context['departments']=departments

            name = request.POST["name"]
            department = request.POST["department"]
            
            if name == "":
                context["message"]="Name cannot be blank!"
                return render(request, template, context=context)

            # Check course name 
            course_exists = Course.objects.filter(name=name).exists()
            if course_exists:
                context["message"]="Course name already exists!"
                return render(request, template, context=context)

            try:
                course = Course(name=name, department_id=department)
                course.save()
                context["message"]="Course added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)

class GetCourses(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "home/list_courses.html"
        listCourses = Course.objects.all()
        context = {
            "courses": listCourses
        }
        return render(request, template, context=context)


# Companies
class AddCompanies(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "LoginRegister/add_company.html"
        return render(request, template)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            template = "LoginRegister/add_company.html"
            context={}

            name = request.POST["name"]
            about = request.POST["about"]
            
            if name == "":
                context["message"]="Name cannot be blank!"
                return render(request, template, context=context)

            # Check company name 
            name_exists = Companies.objects.filter(name=name).exists()
            if name_exists:
                context["message"]="Company name already exists!"
                return render(request, template, context=context)

            try:
                company = Companies(name=name, about=about)
                company.save()
                context["message"]="Company added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)


class GetCompanies(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        template = "home/list_companies.html"
        listCompanies = Companies.objects.all()
        context = {
            "companies": listCompanies
        }
        return render(request, template, context=context)


# Announcements
class AddAnnouncement(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        template = "other/add_announcements.html"
        context = {}
        return render(request, template, context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.method == "POST":
            template = "other/add_announcements.html"
            context={}

            title = request.POST["title"]
            description = request.POST["description"]
            
            if title == "":
                context["message"]="Name cannot be blank!"
                return render(request, template, context=context)

            try:
                announcement = Announcements(title=title, description=description)
                announcement.save()
                context["message"]="Announcement added successfully!"
            except:
                context["message"]="Something went wrong!"

            return render(request, template, context=context)

class GetAnnouncements(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        template = "other/list_announcements.html"
        listAnnouncements = Announcements.objects.all()
        context = {
            "announcements": listAnnouncements
        }
        return render(request, template, context=context)



# APIs

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
   
    def get(self, request, format = None):
        labels = [
            'January',
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July'
            ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data ={
                     "labels":labels,
                     "chartLabel":chartLabel,
                     "chartdata":chartdata,
             }
        return Response(data)


class PlacedUnplaced(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format = None):
        labels = ['Placed', 'Unplaced']
        chartLabel = "DATA"

        totalStudents = User.objects.filter(is_student=True).count()
        placedStudents = User.objects.filter(is_placed=True).count()
        
        unplacedStudents = totalStudents - placedStudents

        chartdata = [placedStudents,unplacedStudents]
        data = {
            "labels":labels,
            "chartLabel": chartLabel,
            "chartdata":chartdata
        }
        return Response(data)