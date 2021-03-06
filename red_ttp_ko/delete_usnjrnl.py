# Name: USN Journal Deletion with fsutil.exe
# RTA: delete_usnjrnl.py
# ATT&CK: T1107
# Description: Uses fsutil to delete the USN journal.

import common
import time

def main():
    message = "Deleting the USN journal may have unintended consequences"
    common.log("WARNING: %s" % message, log_type="!")
    time.sleep(5)
    common.execute(["fsutil", "usn", "deletejournal", "/d", "C:"])
    

if __name__ == "__main__":
    exit(main())
