from flask import request
import logging, os
from logging.handlers import RotatingFileHandler, SMTPHandler

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        os.path.join(basedir, 'logs/blog.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10)

    request_handler = RotatingFileHandler(
        os.path.join(basedir, 'logs/request.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10)

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    request_handler.setFormatter(request_formatter)
    request_handler.setLevel(logging.INFO)
    # mail_handler = SMTPHandler(
    #     mailhost=app.config['MAIL_SERVER'],
    #     fromaddr=app.config['MAIL_USERNAME'],
    #     toaddrs=['ADMIN_EMAIL'],
    #     subject='Bluelog Application Error',
    #     credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    # mail_handler.setLevel(logging.ERROR)
    # mail_handler.setFormatter(request_formatter)

    # if not app.debug:
        # app.logger.addHandler(mail_handler)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(request_handler)