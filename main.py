import time
import psutil
from tkinter import messagebox

bAlert = False
iLimitMax = 95

def listProccess():
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        print(proc.info)

listProccess()

def writeLog(sType):
    with open("alertperf.log", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {sType} usage reached {iLimitMax}%\n")

while True:
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    print(f"CPU: {cpu}% | RAM: {mem}% | Disque: {disk}% | Réseau (reçu/envoyé): {net.bytes_recv/1e6:.2f} / {net.bytes_sent/1e6:.2f} Mo")

    if round(cpu) == iLimitMax and not bAlert:
        bAlert = True
        messagebox.showwarning("Alerte CPU", f"L'utilisation du CPU a atteint ou a dépassé {iLimitMax}% !")
        
        writeLog("CPU")
    elif round(mem) == iLimitMax and not bAlert:
        bAlert = True
        messagebox.showwarning("Alerte RAM", f"L'utilisation de la RAM a atteint ou a dépassé {iLimitMax}% !")

        writeLog("RAM")
    elif (cpu < iLimitMax and mem < iLimitMax) and bAlert:
        bAlert = False

    time.sleep(0.1)
