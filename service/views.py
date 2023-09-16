from django.urls import reverse_lazy, reverse
from django.views import generic
from django.utils.text import slugify
from service import models
from service.forms import ClientForm, MailingForm, MessageForm, BlogForm
from service.models import Client, Message, Blog, MailingLogs, Mailing
from service.services import get_posts_cached
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import mixins
from django.http import Http404


class EditCheckMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('Изменять может только владелец')
        return self.object


class SetUserMixin:
    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PermissionAndLoginRequiredMixin(PermissionRequiredMixin, LoginRequiredMixin):
    model = models.Mailing


class MainView(generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mailings_total'] = Mailing.objects.count()
        context['mailings_active'] = Mailing.objects.filter(is_active=True).count()
        unique_clients = []
        for client in Client.objects.all():
            if client.mailing_set.count() == 1:
                unique_clients.append(client.name)
        context['unique_clients'] = ', '.join(unique_clients)
        context['posts'] = get_posts_cached(3)

        return context


class ClientCreateView(SetUserMixin, generic.CreateView):
    # permission_required = 'service.create_client'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients')
    extra_context = {
        'title': 'Создание клиента рассылки'
    }


class ClientsView(generic.ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты для рассылки'
    }


class ClientDeleteView(EditCheckMixin, generic.DeleteView):
    # permission_required = 'service.delete_client'
    model = Client
    success_url = reverse_lazy('service:clients')
    extra_context = {
        'title': 'Удалить клиента'
    }


class ClientUpdateView(EditCheckMixin, generic.UpdateView):
    # permission_required = 'service.change_client'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:clients')
    extra_context = {
        'title': 'Изменить данные клиента'
    }


class MailingCreateView(PermissionRequiredMixin, SetUserMixin, generic.CreateView):
    permission_required = 'service.add_mailing'
    model = models.Mailing
    form_class = MailingForm

    success_url = reverse_lazy('service:mailing_list')
    extra_context = {
        'title': 'Создание рассылки'
    }


class MailingsView(generic.ListView):
    model = models.Mailing
    extra_context = {
        'title': 'Рассылки',
    }


class MailingDeleteView(PermissionAndLoginRequiredMixin, EditCheckMixin, generic.DeleteView):
    permission_required = 'service.delete_mailing'
    model = models.Mailing
    success_url = reverse_lazy('service:mailing_list')
    extra_context = {
        'title': 'Удалить рассылку'
    }


class MailingUpdateView(PermissionAndLoginRequiredMixin, EditCheckMixin, generic.UpdateView):
    permission_required = 'service.change_mailing'
    model = models.Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:mailing_list')
    extra_context = {
        'title': 'Изменить данные рассылки'
    }


class MailingAttemptsView(generic.ListView):
    model = MailingLogs
    extra_context = {
        'title': 'Завершенные рассылки'
    }


class MessageCreateView(PermissionRequiredMixin, SetUserMixin, generic.CreateView):
    permission_required = 'service.add_message'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:messages')
    extra_context = {
        'title': 'Создание сообщения'
    }


class MessagesView(generic.ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения'
    }


class MessageDeleteView(PermissionRequiredMixin, EditCheckMixin, generic.DeleteView):
    permission_required = 'service.delete_mailing'
    model = Message
    success_url = reverse_lazy('service:messages')
    extra_context = {
        'title': 'Удалить сообщение'
    }


class MessageUpdateView(PermissionRequiredMixin, EditCheckMixin, generic.UpdateView):
    permission_required = 'service.change_message'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:messages')
    extra_context = {
        'title': 'Изменить сообщение'
    }


class BlogPostCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'service.add_post'
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('service:blog')
    extra_context = {
        'title': 'Создание статьи'
    }

    def form_valid(self, form):
        if form.is_valid:
            fields = form.save(commit=False)
            string = fields.title.translate(
                str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                              "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
            fields.slug = slugify(string)
            fields.save()
        return super().form_valid(form)


class BlogView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogPostDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        post = super().get_object()
        post.add_view()
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр статьи'
        return context_data


class BlogPostUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'service.change_post'
    model = Blog
    form_class = BlogForm

    extra_context = {
        'title': 'Изменить статью'
    }

    def get_success_url(self):
        return reverse('service:post', args=[*self.kwargs.values()])


class BlogPostDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'service.delete_post'
    model = Blog
    extra_context = {
        'title': 'Удаление'
    }
    success_url = reverse_lazy('service:blog')
