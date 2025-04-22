
import os
import time

def flash_usb_drive(drive_letter="E:"):
    try:
        while True:
            os.system(f"powershell (Get-Volume -DriveLetter {drive_letter[0]}).DriveType")
            print(f"USB {drive_letter} check-in.")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping USB signal loop.")

if __name__ == "__main__":
    flash_usb_drive()
