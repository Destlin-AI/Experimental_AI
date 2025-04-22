
import wmi
import time

w = wmi.WMI(namespace="root\wmi")

def monitor_and_adjust():
    while True:
        temps = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
        celsius = (temps / 10.0) - 273.15
        print(f"🌬️ CPU Temp: {celsius:.1f}°C")
        if celsius > 70:
            print("💨 Boost fan via system override.")
        time.sleep(5)

if __name__ == "__main__":
    monitor_and_adjust()
