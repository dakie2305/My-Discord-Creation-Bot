import datetime
import logging
import os

def get_logger(name, trace_dir="Traces"):
  """
  Creates a logger that writes to a file named after the current date within a Traces folder.

  Args:
      name: The name of the logger
      traces_folder: The directory name for storing logs (default: "Traces")

  Returns:
      A logging.Logger object
  """
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  traces_folder = os.path.join(os.path.dirname(__file__), trace_dir)
  # Create the Traces folder if it doesn't exist
  os.makedirs(traces_folder, exist_ok=True)  # Handles existing folder gracefully

  handler = logging.FileHandler(os.path.join(traces_folder, f"{name}-{datetime.date.today()}.log"), mode='a', encoding='utf-8')
  handler.setFormatter(formatter)

  # Check if the file already exists for the current day
  current_date = os.path.splitext(handler.baseFilename)[0].split('_')[-1]
  if not os.path.exists(handler.baseFilename) or current_date != str(datetime.date.today()):
    # Create a new file if it doesn't exist or if it's a new day
    handler.close()
    handler = logging.FileHandler(os.path.join(traces_folder, f"{name}-{datetime.date.today()}.log"), mode='w', encoding='utf-8')
    handler.setFormatter(formatter)

  logger = logging.getLogger(name)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)  # Adjust the logging level as needed
  return logger