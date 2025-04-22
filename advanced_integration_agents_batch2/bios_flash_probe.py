
import subprocess

def read_bios_serial():
    try:
        output = subprocess.check_output("wmic bios get serialnumber", shell=True)
        print("🔐 BIOS Serial:
", output.decode())
    except Exception as e:
        print("⚠️ BIOS read failed:", e)

if __name__ == "__main__":
    read_bios_serial()
