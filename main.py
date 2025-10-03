import time
import psutil
from tkinter import messagebox

bAlert = False
iLimitMax = 95

def listProccess():

    tList = []
    for proc in psutil.process_iter(['pid', 'name']):
        oProccess = psutil.Process(proc.info['pid'])

        cpu = oProccess.cpu_percent(interval=0.1)  # Initial call to set up the measurement

        if cpu == 0.0 or cpu is None or proc.info['name'] == "System Idle Process":
            continue

        mem = oProccess.memory_percent()
        disk = oProccess.io_counters()
        tList.append((proc.info['name'], cpu, mem, disk.read_bytes, disk.write_bytes))

    tList.sort(key=lambda x: x[1], reverse=True)

    return tList[:10]

def writeLog(sType):
    with open("alertperf.log", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {sType} usage reached {iLimitMax}%\n")

        for proc in listProccess():
            f.write(f"Processus: {proc[0]} | CPU: {proc[1]}% | RAM: {proc[2]}% | Disque (lu/écrit): {proc[3]/1e6:.2f} / {proc[4]/1e6:.2f} Mo\n")

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
