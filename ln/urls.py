"""lingnengOA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import Login, Check_announcement, Send_announcement, Offer_userinfo, Offer_entering, Search_name, Update_userinfo, All_userinfo, Leave_api, Offer_leader, All_Leave, Announcement_content
from django.urls import path, re_path

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('check_announcement/',
         Check_announcement.as_view(),
         name='check_announcement'),
    path('send_announcement/',
         Send_announcement.as_view(),
         name='send_announcement'),
    path('offer_entering/',
         Offer_entering.as_view(),
         name='Offer_entering'),
    path('offer_userinfo/',
         Offer_userinfo.as_view(),
         name='Offer_userinfo'),
    path('search_name/',
         Search_name.as_view(),
         name='Search_name'),
    path('update_userinfo/',
         Update_userinfo.as_view(),
         name='update_userinfo'),
    path('all_userinfo/',
         All_userinfo.as_view(),
         name='All_userinfo'),
    path('leave_api/',
         Leave_api.as_view(),
         name='leave_api'),
    path('offer_leader/',
         Offer_leader.as_view(),
         name='offer_leader'),
    path('all_leave/',
         All_Leave.as_view(),
         name='all_leave'),
    path('announcement_content/',
         Announcement_content.as_view(),
         name='announcement_content'),
]
