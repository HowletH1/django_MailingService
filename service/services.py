from datetime import datetime
from smtplib import SMTPException
from django.core.cache import cache
from django.core.mail import send_mail, send_mass_mail
from django_MailingService import settings
from service.models import Mailing, MailingLogs, Blog, Message, Client


def get_posts_cached(n: int):
    if settings.CACHE_ENABLED:
        key = 'posts'
        posts = cache.get(key)
        if posts is None:
            posts = Blog.objects.all()
            cache.set(key, posts)
    else:
        posts = Blog.objects.all()
    return posts.order_by('?')[:n]


def check_mailing_time():
    mailings = Mailing.objects.all() \
        .filter(date__lte=datetime.today()) \
        .filter(time__lte=datetime.now()) \
        .filter(status='CR')
    print(mailings)
    for mailing in mailings:
        clients = Client.objects.filter(mailing=mailing.pk)
        messages = Message.objects.filter(mailing=mailing.pk)
        emails = [client.email for client in clients]
        mass_messages = []
        for message in messages:
            mass_messages.append((message.title, message.body, settings.EMAIL_HOST_USER, emails))
        print(mass_messages)
        sendmail(mass_messages, mailing)
        # добавить 1 день если ежедневно
        # вычислимть слкед дату


def sendmail(mass_messages, mailing_pk):
    mailing_log = MailingLogs(mailing=mailing_pk)
    try:
        response = send_mass_mail(mass_messages, fail_silently=False)
    except Exception as e:
        mailing_log.server_request = str(e)
        mailing_log.status = False
    else:
        mailing_log.server_request = 'Success'
        mailing_log.status = True
    mailing_log.save()


