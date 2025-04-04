# custom_handlers.py
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
    """

    def doRollover(self):
        super().doRollover()

        # Compress each rotated backup file
        for i in range(self.backupCount, 0, -1):
            log_filename = f"{self.baseFilename}.{i}"
            if os.path.exists(log_filename):
                # Generate a timestamp for the filename.
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                compressed_filename = f"{log_filename}.{timestamp}.gz"
                with open(log_filename, 'rb') as f_in, gzip.open(compressed_filename, 'wb') as f_out:
                    f_out.writelines(f_in)
                os.remove(log_filename)

        # Cleanup: Remove older compressed files if they exceed backupCount.
        # Use glob to find all gz files that match the rotated log file pattern.
        gz_pattern = f"{self.baseFilename}.*.gz"
        gz_files = glob.glob(gz_pattern)
        if len(gz_files) > self.backupCount:
            # Sort the files by modification time (oldest first)
            gz_files.sort(key=os.path.getmtime)
            # Remove the oldest files beyond the backupCount limit
            for old_file in gz_files[:-self.backupCount]:
                os.remove(old_file)
