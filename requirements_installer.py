required = [
    "torch",
    "numpy",
    "ray",
    "optuna",
    "matplotlib",
    "psutil",
    "pyyaml"
]

def install_all():
    import subprocess
    for r in required:
        print(f"[INSTALL] Installing: {r}")
        subprocess.run(["pip", "install", r])

if __name__ == "__main__":
    install_all()
