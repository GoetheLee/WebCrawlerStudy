import os
import time
import calendar

print(os.environ['PATH'])
print(os.getcwd())
os.chdir('..')
print(os.getcwd())

print(calendar.calendar(2017))

for i in range(1, 10):
    print(time.localtime())
    print(time.asctime(time.localtime()))
    time.sleep(1)

