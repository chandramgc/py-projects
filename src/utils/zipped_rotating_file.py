import os
import logging.handlers
import zipfile
import datetime


class ZippedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    A RotatingFileHandler that compresses the rotated log files.
    """

    def doRollover(self):
        """
        Performs log rollover and compresses the rotated log file.
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            # Shift backup files.
            for i in range(self.backupCount - 1, 0, -1):
                sfn = f"{self.baseFilename}.{i}"
                dfn = f"{self.baseFilename}.{i + 1}"
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            # Rotate the current log file.
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)

            # Create a ZIP archive of the rotated log file.
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"{dfn}_{timestamp}.zip"
            with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(dfn, arcname=os.path.basename(dfn))
            os.remove(dfn)

        # Reopen the log file for writing.
        self.mode = "w"
        self.stream = self._open()
