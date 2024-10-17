from django.urls import path
from .views import Home, Login, Register, Logout, GetUsers, Profile, GetDrives, Drive, UpdateDrive, DeleteDrive, NewDrive, ApplyDrive, DriveResponses, NewCoordinator, Coordinators

from .views import AddDepartment, GetDepartments, AddCourse, GetCourses, AddCompanies, GetCompanies, AddAnnouncement, GetAnnouncements

urlpatterns = [
    # 404 ERROR PAGE
    # path('ERROR', Error.as_view(), name="error"),

    path('', Home.as_view(), name="homepage"),

    # USER AUTHENTICATION & REGISTRATION
    path('login/', Login.as_view(), name="login"),
    path('register/', Register.as_view(), name="register"),
    path('logout/', Logout.as_view(), name="logout"),

    path('users/', GetUsers.as_view(), name="users"),
    path('profile/<str:id>/', Profile.as_view(), name="profile"),
    # path('user/', GetUsers.as_view(), name="users"),
    
    path('drives/', GetDrives.as_view(), name="drives"),
    path('drives/<int:id>/', Drive.as_view(), name="drive"),
    path('drives/<int:id>/apply/', ApplyDrive.as_view(), name='apply_drive'),
    path('drives/<int:id>/update/', UpdateDrive.as_view(), name="update_drive"),
    path('drives/<int:id>/delete/', DeleteDrive.as_view(), name="delete_drive"),
    path('drives/<int:id>/responses/', DriveResponses.as_view(), name="drive_responses"),
    path('newdrive/', NewDrive.as_view(), name="create_drive"),
    path('applydrive/<int:id>', ApplyDrive.as_view(), name='apply_drive'),

    path('newcoordinator/', NewCoordinator.as_view(), name="create_coordinator"),
    path('coordinators/', Coordinators.as_view(), name="coordinators"),

    path('departments/add/', AddDepartment.as_view(), name="add_departments"),
    path('departments/list/', GetDepartments.as_view(), name="list_departments"),

    path('courses/add/', AddCourse.as_view(), name="add_courses"),
    path('courses/list/', GetCourses.as_view(), name="list_courses"),

    path('companies/add/', AddCompanies.as_view(), name="add_companies"),
    path('companies/list/', GetCompanies.as_view(), name="list_companies"),

    
    path('announcements/add/', AddAnnouncement.as_view(), name="add_announcements"),
    path('announcements/list/', GetAnnouncements.as_view(), name="list_announcements"),
]
