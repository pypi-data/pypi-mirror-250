from . import logging

__version__ = "0.1.0"

# Declare what each of our functions will be referenced as when using zazzle.'function' syntax
configure_logger = logging.ZZ_Logging.configure_logger
log = logging.ZZ_Logging.log
log_wide = logging.ZZ_Logging.log_wide

delete_old_log_files = logging.ZZ_Files.delete_old_log_files

colors = logging.ZZ_Colors