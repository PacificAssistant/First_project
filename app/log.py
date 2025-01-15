import logging
import os

log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Logging')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

general_logger = logging.getLogger('general')
general_logger.setLevel(logging.INFO)

log_file = os.path.join(log_dir, 'general.log')
file_handler = logging.FileHandler(log_file)

file_handler.setLevel(logging.INFO)

# Format for the first logger
file_formatter = logging.Formatter('%(asctime)s %(levelname)s [GENERAL] %(message)s')
file_handler.setFormatter(file_formatter)

# Adding a handler to the first logger
general_logger.addHandler(file_handler)

##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##


# Setting up a second logger (e.g. for errors)
error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)

log_file = os.path.join(log_dir, 'errors.log')
error_file_handler = logging.FileHandler(log_file)

error_file_handler.setLevel(logging.ERROR)

error_file_formatter = logging.Formatter('%(asctime)s %(levelname)s [ERROR] %(message)s')
error_file_handler.setFormatter(error_file_formatter)

error_logger.addHandler(error_file_handler)

user_log = logging.getLogger('user')
user_log.setLevel(logging.INFO)
log_file = os.path.join(log_dir, 'user.log')
user_file_handler = logging.FileHandler(log_file)
user_file_handler.setLevel(logging.INFO)
user_file_formatter = logging.Formatter()
user_file_handler.setFormatter(user_file_formatter)
user_log.addHandler(user_file_handler)


def check(code: int = 0, username='user', admin=0):
    if code == 1:
        user_file_formatter = logging.Formatter('%(message)s' f'{username}' "on" '%(asctime)s' "1")
        user_file_handler.setFormatter(user_file_formatter)
        user_log.addHandler(user_file_handler)
        return user_log
    elif code == 2:
        user_file_formatter = logging.Formatter('%(message)s' f'{username}' "on" '%(asctime)s "2')
        user_file_handler.setFormatter(user_file_formatter)
        user_log.addHandler(user_file_handler)
        return user_log
    else:
        user_file_formatter = logging.Formatter()
        user_file_handler.setFormatter(user_file_formatter)
        user_log.addHandler(user_file_handler)
        return user_log
