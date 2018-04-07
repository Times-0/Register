import argparse

TimelineArgParser = argparse.ArgumentParser(description='Details for MySQL, Recaptcha and APILayer credentials to use with Timeline Signup.')
OptionalArgs = TimelineArgParser.add_argument_group('Optional Arguments')

OptionalArgs.add_argument('-u',  action='store', dest='mysql_usernamae', default='root', help='Username for MySQL server')
OptionalArgs.add_argument('-p',  action='store', dest='mysql_password', default='', help='Password for MySQL server')
OptionalArgs.add_argument('-db',  action='store', dest='mysql_database', default='times-cp', help='MySQL database name')

OptionalArgs.add_argument('-es',  action='store', dest='smtp_server', default=None, help='Your email provider\'s SMTP Server detail')
OptionalArgs.add_argument('-en',  action='store', dest='smtp_user', default=None, help='SMTP username provided by email host')
OptionalArgs.add_argument('-ep',  action='store', dest='smtp_pass', default='', help='SMTP password for the given username')

OptionalArgs.add_argument('-a',  action='store', dest='api_layer', default='b178baae9acc886234b5df63540018dd', help='API Layer\'s key')
OptionalArgs.add_argument('-r',  action='store', dest='recaptcha', default='6Leo6UYUAAAAAHCMUnknbx5m6z-Pw94MOeO1_Y8V', help='Recaptcha\'s security key')

args = TimelineArgParser.parse_args()

MYSQL_USER = args.mysql_usernamae
MYSQL_PASS = args.mysql_password
MYSQL_DB = args.mysql_database

EMAIL_SMTP_SERVER_NAME = args.smtp_server
EMAIL_SMTP_USERNAME = args.smtp_user
EMAIL_SMTP_PASSWORD = args.smtp_pass

API_LAYER_KEY = args.api_layer

RECAPTCHA_SECRET = args.recaptcha