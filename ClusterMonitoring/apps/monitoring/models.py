from django.db import models


# Create your models here.

class Server(models.Model):
    IP = models.CharField(max_length=15, primary_key=True)
    Name = models.CharField(max_length=50)

    def __str__(self):
        string = "{0}"
        return string.format(self.Name)


class ServerInformation(models.Model):
    IP = models.ForeignKey(Server, on_delete=models.CASCADE)
    Date = models.DateTimeField()
    Architecture = models.CharField(max_length=100)
    CpuName = models.CharField(max_length=200)
    Cores = models.IntegerField()
    RamTotal = models.IntegerField()
    RamUsed = models.IntegerField()
    RamPercentage = models.FloatField(default=0)
    AvgCpu1 = models.FloatField(default=0)
    AvgCpu5 = models.FloatField(default=0)
    AvgCpu15 = models.FloatField(default=0)
    IsHtcondor = models.BooleanField(default=False)
    IsHtcondorMaster = models.BooleanField(default=False)
    IsHtcondorSubmit = models.BooleanField(default=False)

    def __str__(self):
        string = "{0}"
        return string.format(self.IP)
