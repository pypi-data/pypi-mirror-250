import logging
import os
import datetime
import traceback
import sys
from zazzle.globals import Variables

# Setting up global variables
gl_log_directory = Variables.gl_log_directory
gl_log_name = Variables.gl_log_name
gl_log_format = Variables.gl_log_format
gl_log_write_method = Variables.gl_log_write_method
gl_log_level = Variables.gl_log_level

# PIPE = "│"
# ELBOW = "└──"
# TEE = "├──"
# PIPE_PREFIX = "│   "
# SPACE_PREFIX = "    "

# ===================================================
# Function Name: test
# Description: A test function for log parameters.
# Input values: N/A
# Output values: N/A
# ===================================================
def test():
	configure_logger = ZZ_Init.configure_logger
	log = ZZ_Logging.log
	try:
		#configure_logger(directory="C:/ah", file_name="my_log", log_format="|{levelname:<8s}| >   {message:s}", file_mode="w", level=2)
		configure_logger()
		log(1, "Hello world!")
		log(3, "Hello world!")
	except:
		log(4, f"This is a 'CRITICAL' message.")

# ===========================================================================================
# Class Name: ZZ_Init
# Description: Bucket for initialization functions
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Init():
	# ===================================================
	# Function Name: set_log_file_name
	# Description: Sets the global variable 'gl_log_file_name' to the name input by the user.
	# Input values: input_log_file_name(string)
	# Output values: N/A
	# ===================================================
	def set_log_file_name(input_log_file_name):
		log = ZZ_Logging.log

		try:
			global gl_log_file_name
			gl_log_file_name = input_log_file_name
	
		except:
			log(4, "COULDN'T SET LOG NAME")

	# ===================================================
	# Function Name: set_log_directory
	# Description: Sets the global variable 'gl_log_directory' to the directory input by the user.
	# Input values: input_log_directory(string)
	# Output values: N/A
	# ===================================================
	def set_log_directory(input_log_directory):
		log = ZZ_Logging.log

		try:
			global gl_log_directory
			gl_log_directory = input_log_directory
	
		except:
			log(4, "COULDN'T SET LOG DIRECTORY")

	# ===================================================
	# Function Name: set_log_format
	# Description: Sets the global variable 'gl_log_format' to the format input by the user.
	# Input values: input_log_directory(string)
	# Output values: N/A
	# ===================================================
	def set_log_format(input_log_format):
		log = ZZ_Logging.log

		try:
			global gl_log_format
			gl_log_format = input_log_format
	
		except:
			log(4, "COULDN'T SET LOG DIRECTORY")

	# ===================================================
	# Function Name: set_log_file_mode
	# Description: Sets the logging method for the logger (example: appending messages vs. writing a new file)
	# Input values: input_write_method(string)
	# Output values: N/A
	# ===================================================
	def set_log_file_mode(input_file_mode):
		log = ZZ_Logging.log
		
		try:
			global gl_log_write_method
			gl_log_write_method = input_file_mode
	
		except:
			log(4, "COULDN'T SET WRITE METHOD")

	# ===================================================
	# Function Name: set_log_level
	# Description: Sets the logging level
	# Input values: input_log_level(int)
	# Output values: N/A
	# ===================================================
	def set_log_level(input_log_level):
		log = ZZ_Logging.log
		
		try:
			global gl_log_level
			if input_log_level == 0:
				gl_log_level = logging.DEBUG
			elif input_log_level == 1:
				gl_log_level = logging.INFO
			elif input_log_level == 2:
				gl_log_level = logging.WARNING
			elif input_log_level == 3:
				gl_log_level = logging.ERROR
			elif input_log_level == 4:
				gl_log_level = logging.CRITICAL
			else:
				gl_log_level = logging.DEBUG

		except:
			log(4, "COULDN'T SET LOG LEVEL")

	# ===================================================
	# Function Name: configure_logger
	# Description: Runs the basic configuration for the logger
	# Input values: N/A
	# Output values: N/A
	# ===================================================
	def configure_logger(file_name=None, directory=None, log_format=None, file_mode=None, level=None):

		# Run our input parsing functions
		ZZ_Init.set_log_file_name(file_name)
		ZZ_Init.set_log_directory(directory)
		ZZ_Init.set_log_format(log_format)
		ZZ_Init.set_log_file_mode(file_mode)
		ZZ_Init.set_log_level(level)

		# Configure
		try:
			# Check for a custom directory input
			if gl_log_directory:
				config_path = gl_log_directory
			else:
				user = os.getlogin()
				config_path = f"C:/Users/{user}/Documents/Zazzle"

			# Make the directory if it doesn't exist already
			if os.path.exists(config_path):
				pass
			else:
				os.makedirs(config_path)

			# Check for a custom file name input
			if gl_log_file_name:
				config_name = f"{gl_log_file_name}.log"
			else:
				now = datetime.datetime.now()
				config_name = now.strftime(f"%Y-%m-%d.log")

			file_name = f"{config_path}/{config_name}"

			# Check for a custom internal log format
			if gl_log_format:
				config_format = gl_log_format
			else:
				config_format = "{asctime:s} | {levelname:<8s} | >   {message:s}"

			# Check for a custom log write method
			if gl_log_write_method:
				config_file_mode = gl_log_write_method
			else:
				config_file_mode = "w"

			# Check for a custom log level
			if gl_log_level:
				config_log_level = gl_log_level
			else:
				config_log_level = logging.DEBUG

			# Configure our logs based on user inputs
			logging.basicConfig(filename=file_name, filemode=config_file_mode, format=config_format, style='{', level=config_log_level, force=True)
	
		except:
			print('COULD NOT CONFIGURE LOGGER')

# ===========================================================================================
# Class Name: SL_Files
# Description: Bucket for functions focused on file manipulation.
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Files():

	# ===================================================
	# Function Name: delete_old_log_files
	# Description: Searches for and deletes any old log files detected in the currently set log directory
	# Input values: keep_amount(int)
	# Output values: N/A
	# ===================================================
	def delete_old_log_files(keep_amount=5):
		global gl_log_directory
		global gl_log_file_name
		logs = []
		oldest_file = []
		log = ZZ_Logging.ah_log

		try:
			# Scan the log directory for all files, and isolate any files that end with '.log'
			directory_scan = os.listdir(gl_log_directory)
			for i in directory_scan:
				if ".log" in i:
					logs.append(i)

			for i in range(len(logs)):
				logs[i] = f"{os.getcwd()}\{logs[i]}"
			full_path = ["{0}".format(x) for x in logs]

			if len(logs) > keep_amount:
				oldest_file.append(min(full_path, key=os.path.getctime))
				os.remove(oldest_file[0])

		except:
			log(4, "UNABLE TO DELETE OLD LOG FILES")

# ===========================================================================================
# Class Name: ZZ_Logging
# Description: Bucket for logging functions
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class ZZ_Logging():
	# ===================================================
	# Function Name: log
	# Description: Takes a log level and a message for the logger. Logs to a file.
	# Input values: input_level(int), log_message(string)
	# Output values: N/A
	# ===================================================
	def log(input_level=0, log_message="I'm an empty log message!", flag=True):
		try:
			# Debug
			if input_level == 0:
				# String variables
				color = SL_Colors.fg.darkgrey
				reset = SL_Colors.reset
				flag_text = f"| {'DEBUG':<8s} |\t"

				# Print the level flag if enabled
				if flag:
					print(f"{color}{flag_text}{log_message}{reset}")
				else:
					print(f"{color}{log_message}{reset}")

				# Write to the log file
				logging.debug(log_message)

				# Pytest check
				check = True

			# Info
			elif input_level == 1:
				# String variables
				color = SL_Colors.fg.green
				reset = SL_Colors.reset
				flag_text = f"|{'INFO':<8s}|\t"

				# Print the level flag if enabled
				if flag:
					print(f"{color}{flag_text}{log_message}{reset}")
				else:
					print(f"{color}{log_message}{reset}")

				# Write to the log file
				logging.info(log_message)

				# Pytest check
				check = True

			# Warning
			elif input_level == 2:
				# String variables
				color = SL_Colors.fg.yellow
				reset = SL_Colors.reset
				flag_text = f"|{'WARNING':<8s}|\t"

				# Print the level flag if enabled
				if flag:
					print(f"{color}{flag_text}{log_message}{reset}")
				else:
					print(f"{color}{log_message}{reset}")

				# Write to the log file
				logging.warning(log_message)

				# Pytest check
				check = True

			# Error
			elif input_level == 3:
				# String variables
				color = SL_Colors.fg.red
				reset = SL_Colors.reset
				flag_text = f"|{'ERROR':<8s}|\t"

				# Print the level flag if enabled
				if flag:
					print(f"{color}{flag_text}{log_message}{reset}")
				else:
					print(f"{color}{log_message}{reset}")

				# Write to the log file
				logging.error(log_message)

				# Pytest check
				check = True

			# Critical
			elif input_level == 4:
				# String variables
				color = SL_Colors.fg.red
				reset = SL_Colors.reset
				underline = SL_Colors.underline
				flag_text = f"|{'CRITICAL':<8s}|\t"
				exc = traceback.format_exc()

				# Print the level flag if enabled
				if flag:
					print(f"{color}{underline}{flag_text}{log_message}{reset}")
				else:
					print(f"{color}{underline}{log_message}{reset}")

				print(f"{color}{exc}{reset}")

				# Write to the log file
				logging.exception(log_message)

				# Pytest check
				check = True

			# Anything else prints as a debug message
			else:
				color = SL_Colors.fg.darkgrey
				reset = SL_Colors.reset
				flag_text = f"|{'DEBUG':<8s}|\t"

				if flag:
					print(f"{SL_Colors.fg.darkgrey}{log_message}{SL_Colors.reset}")
					logging.debug(log_message)
					check = True
				else:
					print(f"{SL_Colors.fg.darkgrey}{flag_text}{log_message}{SL_Colors.reset}")
					logging.debug(log_message)

		# If something goes wrong, get the traceback and log to both the console and the log
		except:
			print(f"{SL_Colors.fg.red}{log_message}{SL_Colors.reset}")
			exc = traceback.format_exc()
			print(f"{SL_Colors.fg.red}{exc}{SL_Colors.reset}")
			logging.exception(log_message)
			check = False

		return(check)

	# ===================================================
	# Function Name: log_wide
	# Description: Logs a string at the specified level, console width, and character.
	# Input values: log_level(int), log_message(string), log_width(int), log_character(string)
	# Output values: N/A
	# ===================================================
	def log_wide(log_level=0, log_message="", log_width=None, log_character="*"):

		# There's definitley a better way to do this

		log = ZZ_Logging.log

		if log_width == None:
			log_width = os.get_terminal_size().columns
		
		if log_width > 110:
			log_width = 110
		
		log(log_level, f"{log_message:{log_character}^{log_width}}", False)

	# ===================================================
	# Function Name: get_func_name
	# Description: Returns the name of the function it was run from.
	# Input values: frame(int)
	# Output values: name(string)
	# ===================================================
	def get_func_name(frame=0):
		try:
			name = sys._getframe(frame).f_code.co_name
			return(name)
	
		except:
			log = ZZ_Logging.log
			log(4, f"CAN'T GET FUNCTION NAME")

# ===========================================================================================
# Class Name: SL_Colors
# Description: Bucket for foreground, background, and modifiers for console colors
# Input values: N/A
# Output values: N/A
# ===========================================================================================
class SL_Colors():
	reset = '\033[0m'
	bold = '\033[01m'
	disable = '\033[02m'
	underline = '\033[04m'
	reverse = '\033[07m'
	strikethrough = '\033[09m'
	invisible = '\033[08m'

	# ===========================================================================================
	# Class Name: fg
	# Description: Bucket for foreground console colors.
	# Input values: N/A
	# Output values: N/A
	# ===========================================================================================
	class fg:
		black = '\033[30m'
		red = '\033[31m'
		green = '\033[32m'
		orange = '\033[33m'
		blue = '\033[34m'
		purple = '\033[35m'
		cyan = '\033[36m'
		lightgrey = '\033[37m'
		darkgrey = '\033[90m'
		lightred = '\033[91m'
		lightgreen = '\033[92m'
		yellow = '\033[93m'
		lightblue = '\033[94m'
		pink = '\033[95m'
		lightcyan = '\033[96m'

	# ===========================================================================================
	# Class Name: bg
	# Description: Bucket for background console colors.
	# Input values: N/A
	# Output values: N/A
	# ===========================================================================================
	class bg:
		black = '\033[40m'
		red = '\033[41m'
		green = '\033[42m'
		orange = '\033[43m'
		blue = '\033[44m'
		purple = '\033[45m'
		cyan = '\033[46m'
		lightgrey = '\033[47m'

if __name__ == "__main__":
	#test()
	pass