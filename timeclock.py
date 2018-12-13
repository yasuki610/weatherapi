from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

#間隔は1分ごとにしています
#minutesではなくてhourに変更したら、時間での指定も可能です
@sched.scheduled_job('interval', minutes=1)
def timed_job():
	print("Let's start")
	os.system("python weatherapisample.py")


sched.start()
