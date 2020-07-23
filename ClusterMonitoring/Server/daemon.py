import subprocess, requests, datetime, socket, json

ip = subprocess.check_output(['hostname', '-i']).decode('utf-8').strip()

name = subprocess.check_output(['hostname']).decode('utf-8').strip()

fullName = subprocess.check_output(['hostname', '-f']).decode('utf-8').strip()

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def totalMemory():
    free = subprocess.Popen(['free', '-m'], stdout=subprocess.PIPE)
    cutLine = subprocess.Popen(['cut', '-d', ':', '-s', '-f2'], stdin=free.stdout, stdout=subprocess.PIPE)
    head = subprocess.Popen(['head', '-n1'], stdin=cutLine.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=head.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f2'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def usageMemory():
    free = subprocess.Popen(['free', '-m'], stdout=subprocess.PIPE)
    cutLine = subprocess.Popen(['cut', '-d', ':', '-s', '-f2'], stdin=free.stdout, stdout=subprocess.PIPE)
    head = subprocess.Popen(['head', '-n1'], stdin=cutLine.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=head.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f3'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def freeMemory():
    free = subprocess.Popen(['free', '-m'], stdout=subprocess.PIPE)
    cutLine = subprocess.Popen(['cut', '-d', ':', '-s', '-f2'], stdin=free.stdout, stdout=subprocess.PIPE)
    head = subprocess.Popen(['head', '-n1'], stdin=cutLine.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=head.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f4'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def avgCpu1():
    cat = subprocess.Popen(['cat', '/proc/loadavg'], stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f1'], stdin=cat.stdout).decode('utf-8').strip()
    return output


def avgCpu5():
    cat = subprocess.Popen(['cat', '/proc/loadavg'], stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f2'], stdin=cat.stdout).decode('utf-8').strip()
    return output


def avgCpu15():
    cat = subprocess.Popen(['cat', '/proc/loadavg'], stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-s', '-f3'], stdin=cat.stdout).decode('utf-8').strip()
    return output


def cpuName():
    lscpu = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', '-e', 'name'], stdin=lscpu.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=grep.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f3-'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def cpuArch():
    lscpu = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', '-e', 'Arc'], stdin=lscpu.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=grep.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f2-'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def cpuCores():
    lscpu = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', '-e', 'CPU(s):'], stdin=lscpu.stdout, stdout=subprocess.PIPE)
    head = subprocess.Popen(['head', '-n1'], stdin=grep.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=head.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f2-'], stdin=tr.stdout).decode('utf-8').strip()
    return output


def isCondorNode():
    status = subprocess.Popen(['condor_status'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    grep = subprocess.Popen(['grep', socket.gethostname()], stdin=status.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['wc', '-l'], stdin=grep.stdout).decode('utf-8').strip()
    return output


def whoIsCondorMaster():
    status = subprocess.Popen(['condor_status', '-negotiator'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    tail = subprocess.Popen(['tail', '-n', '1'], stdin=status.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f1'], stdin=tail.stdout).decode('utf-8').strip()
    return output


def whoIsCondorSubmit():
    status = subprocess.Popen(['condor_status', '--schedd'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    head = subprocess.Popen(['head', '-n', '3'], stdin=status.stdout, stdout=subprocess.PIPE)
    tail = subprocess.Popen(['tail', '-n', '1'], stdin=head.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f1'], stdin=tail.stdout).decode('utf-8').strip()
    return output


data = {"ip": ip, "name": name, "fullName": fullName, "date": date, "totalMemory": totalMemory(),
        "usageMemory": usageMemory(), "freeMemory": freeMemory(), "avgCpu1": avgCpu1(), "avgCpu5": avgCpu5(),
        "avgCpu15": avgCpu15(), "cpuArch": cpuArch(), "cpuName": cpuName(),"cpuCores": cpuCores(),
        "isCondorNode": isCondorNode(), "condorMaster": whoIsCondorMaster(), "condorSubmit": whoIsCondorSubmit()}


jsonData = json.dumps(data)

jsonSend = json.loads(jsonData)

requests.post('http://172.22.52.18:8000/monitoring/receive', json=jsonSend)
