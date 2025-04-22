
import subprocess

def read_tpm_identity():
    try:
        output = subprocess.check_output("wmic path win32_tpm get /value", shell=True)
        print(output.decode())
    except Exception as e:
        print("TPM access failed:", e)

if __name__ == "__main__":
    read_tpm_identity()
