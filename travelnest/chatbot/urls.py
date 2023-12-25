# chatbot/urls.py

from django.urls import path

from chatbot.views import process_user_input

urlpatterns = [
    path('process_user_input/', process_user_input, name='process_user_input'),
]
