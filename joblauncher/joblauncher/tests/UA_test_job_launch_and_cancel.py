import joblauncher
import time

joblaunch = joblauncher.JobLauncher()
joblaunch.schedule_and_launch_job('bbic_wrapper')
print(joblaunch.launched_job_url)

time.sleep(15)

resp = joblaunch.get_single_job_status()
print(resp)

resp = joblaunch.deallocate_and_cancel_job()
resp.show_response()

print(joblaunch.session_status().show_response())

####

joblaunch.schedule_and_launch_job('bbic_wrapper')
print(joblaunch.launched_job_url)

time.sleep(15)

resp = joblaunch.get_single_job_status()
print(resp)

resp = joblaunch.deallocate_and_cancel_job()
resp.show_response()