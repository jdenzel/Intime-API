from django.urls import path
from . views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('checksession/', CheckSessionView.as_view(), name='checksession'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clockin/', ClockInView.as_view(), name='clockin'),
    path('clockout/<int:id>/', ClockOutView.as_view(), name='clockout'),
    path('timesheet/', TimeSheetView.as_view(), name='timesheet'),
]
