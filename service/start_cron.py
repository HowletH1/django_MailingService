from service.services import start_mailing


def my_scheduled_job():
    start_mailing()
