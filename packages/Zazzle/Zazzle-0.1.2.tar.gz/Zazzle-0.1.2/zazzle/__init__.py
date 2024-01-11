from . import zz_logging

__version__ = "0.1.2"

# Declare what each of our functions will be referenced as when using zazzle.'function' syntax
configure_logger = zz_logging.ZZ_Logging.configure_logger
log = zz_logging.ZZ_Logging.log
log_wide = zz_logging.ZZ_Logging.log_wide

delete_old_log_files = zz_logging.ZZ_Files.delete_old_log_files

colors = zz_logging.ZZ_Colors