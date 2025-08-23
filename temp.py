#!/usr/bin/env python3
import time
import psutil
import subprocess

def get_cpu_temp():
    """Get CPU temperature from thermal zone."""
    try:
        # Raspberry Pi 5 uses cpu-thermal zone
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return temp
    except FileNotFoundError:
        return None

def get_gpu_temp():
    """Get GPU temperature using vcgencmd (if available)."""
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return float(output.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return None

while True:
    cpu_temp = get_cpu_temp()
    gpu_temp = get_gpu_temp()

    print("==== Raspberry Pi 5 Temps ====")
    if cpu_temp is not None:
        print(f"CPU Temp: {cpu_temp:.2f} °C")
    else:
        print("CPU Temp: unavailable")

    if gpu_temp is not None:
        print(f"GPU Temp: {gpu_temp:.2f} °C")
    else:
        print("GPU Temp: unavailable")

    print("==============================\n")
    time.sleep(2)
