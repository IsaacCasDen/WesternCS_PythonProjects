
import re
import datetime
import collections
import os
import threading
import multiprocessing
from multiprocessing import Process, Pool
import calendar
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# match date/time, request type, requested uri, client ip
import time

logs = {}
cpu = multiprocessing.cpu_count()

class LogLine:
    # 00
    # 01
    # 02
    # 03
    # 04
    # 08
    # 11
    # 12

    '2017-06-01 00:00:00 172.16.10.12 GET /mobile/cals/Orientation_Ohio_Creek_Calendar.ics - 80 - 10.1.10.152 Mozilla/5.0 - - 200 0 0 15'
    #regex = r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+([\w\d.]+)\s+([A-Z]+)\s+(.+[\S])\s+"
    regex = r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+[\d\w.]+\s([A-Z]+)\s+([^\s]+)\s+\S+\s+\d+\s+\S+\s([\d\w.]+)"
    extractor = re.compile(regex)

    def __init__(self,line):
        self.line = LogLine.extractor.match(line).groups()

class LogInfo:
    def __init__(self, log:[]=None):
        self.fields = {'SOFTWARE':self.parse_software, 'VERSION':self.parse_version, 'DATE':self.parse_date, 'FIELDS':self.parse_fields}
        self.info = {}
        self.log = []
        self.comment_count = 0
        if logs!=None:
            self.add_lines(log)

    def add_comment(self,comment):
        self.comment_count += 1
        self.info["Comment_" + str(self.comment_count)] = comment

    def parse_software(self, info):
        return info.strip()

    def parse_version(self, info):
        return info.strip()

    def parse_date(self, info):
        return info.strip()

    def parse_fields(self, info):
        return str(info).strip().split(" ")

    def parse_field(self, field: []):
        return self.fields[str(field[0]).upper()](field[1])

    def add_field(self, line):
        if line != None:
            if line.startswith("#"):
                is_comment = False
                if ":" in line:
                    line = str(line[1:])
                    fields = line.split(":", 1)
                    if str(fields[0]).upper() in self.fields:
                        self.info[fields[0]] = self.parse_field(fields)
                    else:
                        is_comment = True
                else:
                    is_comment = True

                if is_comment:
                    self.add_comment(line)

                return True

        return False

    def add_lines(self,lines:[]):
        if lines == None:
            return
        for line in lines:
            self.add_line(line)

    def add_line(self, line: str):
        if line is None:
            return
        if not self.add_field(line):
            log_line = parse_line(line)
            self.log += [log_line]

def parse_line(line):
    """
    Parse a single line using the extractor
    """
    log_line = LogLine(line)
    dt = datetime.datetime.strptime(log_line.line[0], "%Y-%m-%d %H:%M:%S")
    # make a tuple with dt and the rest (splatted)
    return (dt, *log_line.line[1:])

def parse_file(path):
    with open(path, encoding="utf8") as f:
        lines = f.readlines()

    log_info = LogInfo(lines)
    #log_info = LogInfo([parse_line(l) for l in lines])

    return log_info

def run_old(store:{}, id:int, file_path: str, file_key: str):
    data = parse_file(file_path)
    value = (file_key, data)
    store[id] = value

def run(info):
    data = parse_file(info[0])
    value = (info[1], data)
    return value

def read_data():
    path = os.path.join(os.getcwd(), 'weblogs')
    files = [file for file in os.listdir(path)]
    files = files[:7]

    pool = Pool(processes=cpu)
    data_set = [(os.path.join(path, file), str(file)) for i, file in enumerate(files, 1)]

    results = []
    results = pool.map(run, data_set)

    log_id = 0

    for data in results:
        log_key = "log_" + str(log_id)
        if not log_key in logs.keys():
            logs[log_key] = data[1]
        else:
            logs[log_key].log += data[1].log

def get_problem_1(items:[]):
    value = len([val for val in items])
    return value

def get_problem_2(items:[]):
    value = len(collections.Counter([item[3] for item in items]))
    return value

def get_problem_3(items:[]):
    value = [(k,v) for k,v in collections.Counter([datetime.datetime(item[0].year,item[0].month,item[0].day).strftime('%Y-%m-%d') for item in items]).items()]
    return value

def get_problem_4(items:[]):
    value = [(k,v) for k,v in collections.Counter([datetime.datetime(item[0].year,item[0].month,item[0].day,item[0].hour).strftime('%Y-%m-%d %H') for item in items]).items()]
    return value

def get_problem_5(items:[]):
    val = collections.Counter([(item[0].year,item[0].month,item[0].day,item[0].hour,item[3]) for item in items])
    value = [(k,v) for k,v in collections.Counter([datetime.datetime(item[0],item[1],item[2],item[3]).strftime('%Y-%m-%d %H') for item in val.keys()]).items()]
    return value

def plot(data:()):

    m = max([len(item[1]) for item in data])
    #matplotlib.rcParams['figure.figsize']=[m + 1, m + 1]

    #fig = plt.figure()
    #ax1 = fig.add_subplot(2,2,1)
    #ax2 = fig.add_subplot(2,3,1)

    for datum in data:
        #ax1.plot(datum[1],datum[2],datum[4]+'-', label=datum[0])
        #ax2.plot(datum[1],datum[3],datum[4]+'-', label=datum[0])
        plt.plot(datum[1],datum[3],datum[4]+'-', label=datum[0])
    
    plt.legend(loc='upper left')
    #plt.tight_layout()
    #fig=plt.gcf()


    plt.xticks(np.arange(0, m, 1.0))
    plt.savefig('hits.png')
    plt.show()
        
def get_problem_6(items:[]):
    weekday = calendar.day_abbr[:5]
    weekend = calendar.day_abbr[5:]

    _wkday = collections.Counter([datetime.datetime(item[0].year,item[0].month,item[0].day,item[0].hour) for item in items if item[0].strftime('%a') in weekday])
    _wkend = collections.Counter([datetime.datetime(item[0].year,item[0].month,item[0].day,item[0].hour) for item in items if item[0].strftime('%a') in weekend])

    wkday = [(key,_wkday[key]) for key in _wkday.keys()]
    wkend = [(key,_wkend[key]) for key in _wkend.keys()]

    _wkday_hour = {}
    for item in wkday:
        hour = item[0].hour
        if hour in _wkday_hour:
            _wkday_hour[hour] += item[1]
        else:
            _wkday_hour[hour] = item[1]

    _wkend_hour = {}
    for item in wkend:
        hour = item[0].hour
        if hour in _wkend_hour:
            _wkend_hour[hour] += item[1]
        else:
            _wkend_hour[hour] = item[1]

    wkday_hour = sorted([[key,_wkday_hour[key]] for key in _wkday_hour.keys()])
    wkend_hour = sorted([[key,_wkend_hour[key]] for key in _wkend_hour.keys()])

    total = sum([item[1] for item in wkday_hour])
    [item.append(total) for item in wkday_hour]
        
    total = sum([item[1] for item in wkend_hour])
    [item.append(total) for item in wkend_hour]

    value = [['Hour','Weekday','Weekend']]
    values = {}
    for hour in range(24):
        values[hour]=[0,0]

    for item in wkday_hour:
        values[item[0]][0]=round(item[1]/item[2],4)
        

    for item in wkend_hour:
        #values[item[0]][1]=item[1]/item[2]
        values[item[0]][1]=round(item[1]/item[2],4)
        
    for hour in range(24):
        val = values[hour]
        value.append([hour,val[0],val[1]])

    plot((
        ("Weekday", [hour[0] for hour in wkday_hour], [hour[1] for hour in wkday_hour], [hour[1]/hour[2] for hour in wkday_hour],'r'),
        ("Weekend", [hour[0] for hour in wkend_hour], [hour[1] for hour in wkend_hour], [hour[1]/hour[2] for hour in wkend_hour], 'g')))

    #value = ( 
    #    [ 'Weekday', [ ('Hour ' + str(item[0]) + ": ", "{0:.0f}%".format((item[1]/item[2])*100)) for item in wkday_hour ]], 
    #    [ 'Weekend', [ ('Hour ' + str(item[0]) + ": ", "{0:.0f}%".format((item[1]/item[2])*100)) for item in wkend_hour ]] )

    return value

p1=None
p2=None
p3=None
p4=None
p5=None
p6=None

def main():
    read_data()
    for key in logs:
        log_data = logs[key]
        log = log_data.log

        print("Problem 1")
        p1 = get_problem_1(log)
        print(p1)

        print("Problem 2")
        p2 = get_problem_2(log)
        print(p2)

        print("Problem 3")
        p3 = get_problem_3(log)
        print(p3)

        print("Problem 4")
        p4 = get_problem_4(log)
        print(p4)

        print("Problem 5")
        p5 = get_problem_5(log)
        print(p5)

        print("Problem 6")
        p6 = get_problem_6(log)
        print(p6)

if __name__ == "__main__":
    main()

if __name__ == "__main__oldbutnewer":
    manager = multiprocessing.Manager()
    results = manager.dict()
    path = os.path.join(os.getcwd(), 'weblogs')
    files = [file for file in os.listdir(path)]
    processes = list([Process(target=run_old, args=(results, i, os.path.join(path, file), file)) for i, file in enumerate(files, 1) if i < 3])

    processes = processes[:4]

    count_ready = len(processes)
    count_start = 0
    count_done = 0

    for p in processes:
        count_start += 1
        count_ready -= 1
        print(
            "Threads Ready: " + str(count_ready) + ", Threads Started: " + str(count_start) + ", Threads Done: " + str(
                count_done), "         \r")
        p.start()

    for p in processes:
        p.join()
        count_done += 1
        count_start -= 1
        print(
            "Threads Ready: " + str(count_ready) + ", Threads Started: " + str(count_start) + ", Threads Done: " + str(
                count_done), "         \r")

    inn = list(results.values())

    #print(results.values())

    print(logs)

if __name__ == "__main__oldest":
    path = os.path.join(os.getcwd(), 'weblogs')
    file_count = 0
    threads = {'ready':[],'run_old':[],'done':[]}

    for file in os.listdir(path):
        file_count += 1
        thread = Process(target=run_old, args=(logs, os.path.join(path, file), str(file)))
        # thread = Thread_ReadFile(file_count,"Thread_" + str(file),os.path.join(path,file),str(file))
        threads['ready'] += [thread]

    is_run = True
    count_ready = len(threads['ready'])
    count_run = -1
    count_done = -1

    while (count_ready>0):
        count_read = 0
        count_ru = 0
        count_don = 0

        for thread in threads['run_old']:
            if not thread.is_alive():
                threads['run_old'].remove(thread)
                threads['done'] += thread
            else:
                count_ru+=1

        if count_ru<cpu:
            _threads = threads['ready'][:(cpu-count_ru)]
            for thread in _threads:
                thread.start()
            threads['run_old'] += thread
            count_ru+=len(_threads)
            count_read-=len(_threads)

        if count_read != count_ready or count_ru != count_run or count_don != count_done:
            count_read = count_ready
            count_run = count_ru
            count_done = count_don
            print("\nRunning Threads: " + str(count_run) + "\nCompleted Threads: " + str(count_done))



            # logs[file]=parse_file(os.path.join(path,file))

    log_id = 0
    logs_combined = {}

    for key in logs.keys():
        log_key = "log_" + str(log_id)
        if not log_key in logs_combined.keys():
            logs_combined[log_key] = logs[key]
        else:
            logs_combined[log_key].log += logs[key].log

        del logs[key]

        # print(len(set(l[3] for l in logs[key])))

        # dtex=logs[file][10][0]
        # print(datetime.datetime.strftime(dtex,"%Y-%m-%d %H"))

        # collections.Counter(datetime.datetime)
        # break

    print(logs)