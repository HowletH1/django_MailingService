from django.urls import path

from service.apps import ServiceConfig
from service.views import MailingsView, MailingCreateView, MailingUpdateView, ClientsView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, MailingDeleteView, MessagesView, MessageDeleteView, \
    MessageUpdateView, MessageCreateView, BlogView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, \
    BlogPostDeleteView, MainView, ToggleAccount, ToggleMailing

app_name = ServiceConfig.name

urlpatterns = [
    path('', MainView.as_view(template_name='service/main.html'), name='main'),


    path('mailings/', MailingsView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>', ToggleMailing.as_view(), name='toggle_mailing'),

    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='clients_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),
    path('clients/<int:pk>', ToggleAccount.as_view(), name='toggle_account'),

    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='messages_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='messages_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='messages_delete'),

    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/create_post/', BlogPostCreateView.as_view(), name='create_post'),
    path('blog/post/<int:year>/<int:month>/<int:day>/<slug:slug>/', BlogPostDetailView.as_view(), name='post'),
    path('blog/update_post/<int:year>/<int:month>/<int:day>/<slug:slug>/', BlogPostUpdateView.as_view(), name='update_post', ),
    path('blog/delete_post/<int:year>/<int:month>/<int:day>/<slug:slug>/', BlogPostDeleteView.as_view(), name='delete_post'),
]
