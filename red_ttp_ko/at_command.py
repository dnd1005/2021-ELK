#-*- coding: euc-kr -*-
# Name: AT Command Lateral Movement
# RTA: at_command.py
# ATT&CK: T1053
# Description: Enumerates at tasks on target host, and schedules an at job for one hour in the future. Then checks the
#  status of that task, and deletes the task.

from __future__ import print_function
import common
import sys
import datetime
import re


def main(target_host=common.LOCAL_IP):
    host_str = '\\\\%s' % target_host

    # Current time at \\localhost is 11/16/2017 11:25:50 AM
    code, output = common.execute(['net', 'time', host_str])
    match = re.search(r'현재 시간은 (\d+)-(\d+)-(\d+) (오전|오후) (\d+):(\d+):(\d+)', output)
    print(match.groups())
    groups = match.groups()
    y, m, d, period, hh, mm, ss = groups
    now = datetime.datetime(month=int(m), day=int(d), year=int(y), hour=int(hh), minute=int(mm), second=int(ss))
    if period == '오후' and hh != '12':
        now += datetime.timedelta(hours=12)

    # Add one hour minutes
    task_time = now + datetime.timedelta(hours=1)

    # Round down minutes
    time_string = '%d:%d' % (task_time.hour, task_time.minute)

    # Enumerate all remote tasks
    common.execute(['at.exe', host_str])

    # Create a job 1 hour into the future
    code, output = common.execute(['at', host_str, time_string, 'cmd /c echo hello world'])

    if code == 1 and 'deprecated' in output:
        common.log("Unable to continue RTA. Not supported in this version of Windows")
        return common.UNSUPPORTED_RTA

    if code == 0:
        job_id = re.search('ID = (\d+)', output).group(1)

        # Check status and delete
        common.execute(['at.exe', host_str, job_id])
        common.execute(['at.exe', host_str, job_id, '/delete'])


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
