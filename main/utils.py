from marketing import settings


def _log(response):
    with open(settings.TRANSACTION_LOGS_PATH, 'w+') as f:
        f.write(response + "\n")
