from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.monitoring.models import ServerInformation, Server
from django.http import HttpResponse
import json

def landing(request):
    listOfServers = Server.objects.all()
    listToshow = []
    for server in listOfServers:
        data = ServerInformation.objects.filter(IP=server.IP).order_by('-id')[0]
        listToshow.append(data)

    return render(request, 'landing.html', {'servers' : listToshow})

@csrf_exempt
def receive(request):
    if request.method == 'POST':
        data = str(request.body, "utf-8")
        jsonData = json.loads(data)
        savedIp = Server.objects.filter(IP=jsonData["ip"]).exists()
        if not savedIp:
            servercheck = Server(IP=jsonData["ip"], Name=jsonData["name"])
            servercheck.save()
        server = Server.objects.get(pk=jsonData["ip"])
        avgCpu1 = float(jsonData["avgCpu1"]) *100
        avgCpu5 = float(jsonData["avgCpu5"]) *100
        avgCpu15 = float(jsonData["avgCpu15"]) *100
        ramPercentage = round((float(jsonData["usageMemory"]) / float(jsonData["totalMemory"]))*100)
        serverInfo = ServerInformation(IP= server , Date=jsonData["date"],  Architecture=jsonData["cpuArch"],
                                       CpuName=jsonData["cpuName"], Cores=jsonData["cpuCores"],
                                       RamTotal= float(jsonData["totalMemory"]), RamUsed=float(jsonData["usageMemory"]),
                                       RamPercentage= ramPercentage,
                                       AvgCpu1= avgCpu1, AvgCpu5= avgCpu5, AvgCpu15= avgCpu15,
                                       IsHtcondor = True if int(jsonData["isCondorNode"]) > 1 else False,
                                       IsHtcondorMaster= True if jsonData["condorMaster"] == jsonData["fullName"] else False,
                                       IsHtcondorSubmit= True if jsonData["condorSubmit"] == jsonData["fullName"] else False
                                       )

        serverInfo.save()

        return HttpResponse("Listo")
    return redirect('/monitoring')
