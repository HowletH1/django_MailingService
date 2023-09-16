from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.mail import send_mass_mail
from django_MailingService import settings
from service.models import Mailing, MailingLogs, Blog, Message, Client
import datetime
import schedule


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


def sendmail(mass_messages, mailing_pk):
    status = False
    mailing_log = MailingLogs(mailing=mailing_pk)
    try:
        response = send_mass_mail(mass_messages, fail_silently=False)
        status = True
    except Exception as e:
        mailing_log.server_request = str(e)
        mailing_log.status = False
    else:
        mailing_log.server_request = 'Success'
        mailing_log.status = True
        mailing_log.save()
    return status


def start_mailing():
    duration = datetime.timedelta(minutes=5)

    def check_mailing_time():
        delta = datetime.datetime.now() - datetime.datetime.combine(mailing.date, mailing.time)
        return datetime.timedelta() < delta <= duration

    for mailing in Mailing.objects.all():
        clients = Client.objects.filter(mailing=mailing.pk)
        messages = Message.objects.filter(mailing=mailing.pk)
        emails = [client.email for client in clients]
        mass_messages = []
        if mailing.status == 'CR':
            if check_mailing_time():
                mailing.status = 'LA'
                mailing.save()
                for message in messages:
                    mass_messages.append((message.title, message.body, settings.EMAIL_HOST_USER, emails))
                print(mass_messages)
                sendmail(mass_messages, mailing)
                mailing.status = 'CM'
                mailing.save()

        elif mailing.status == 'CM':
            match mailing.frequency:
                case 'DA':
                    mailing.date += datetime.timedelta(days=1)
                case 'WE':
                    mailing.date += datetime.timedelta(days=7)
                case 'MO':
                    mailing.date += datetime.timedelta(days=30)
            mailing.status = 'CR'
            mailing.save()

