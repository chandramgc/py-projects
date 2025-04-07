import gzip
import os
import glob
from datetime import datetime
from logging.handlers import RotatingFileHandler

class CompressingRotatingFileHandler(RotatingFileHandler):
    """
    A rotating file handler that compresses old log files after rollover,
    appending a timestamp to the compressed filename and ensuring that only
    a specified number of compressed files (as defined by backupCount) are kept.

    If a PermissionError occurs during rollover (e.g. the log file is locked),
    the rollover and subsequent archiving are skipped to avoid stopping the Dagster process.
    """
    def doRollover(self):
        try:
            super().doRollover()
        except PermissionError as e:
            # Log the error and skip the rollover; do not propagate the exception.
            return  # Skip the archiving step for this cycle.

        # If rollover succeeds, compress each rotated backup file.
        for i in range(self.backupCount, 0, -1):
            log_filename = f"{self.baseFilename}.{i}"
            if os.path.exists(log_filename):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                compressed_filename = f"{log_filename}.{timestamp}.gz"
                try:
                    with open(log_filename, 'rb') as f_in, gzip.open(compressed_filename, 'wb') as f_out:
                        f_out.writelines(f_in)
                    os.remove(log_filename)
                except Exception as e:
                    return

        # Cleanup: Remove older compressed files if they exceed backupCount.
        gz_pattern = f"{self.baseFilename}.*.gz"
        gz_files = glob.glob(gz_pattern)
        if len(gz_files) > self.backupCount:
            gz_files.sort(key=os.path.getmtime)
            for old_file in gz_files[:-self.backupCount]:
                try:
                    os.remove(old_file)
                except Exception as e:
                    return
