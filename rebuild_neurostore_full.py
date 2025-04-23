import os
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime

# ========== Safe File Writer ==========
def write_file(path_parts, content):
    path = Path(*path_parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote {path}")

# ========== Backup NeuroStore ==========
def backup_neurostore():
    EXPORT_DIR = os.path.expanduser("~/neurostore/backups")
    SOURCE_DIRS = ["agents", "fragments", "logs", "meta", "runtime", "data"]
    os.makedirs(EXPORT_DIR, exist_ok=True)
    backup_name = f"neurostore_brain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    backup_path = os.path.join(EXPORT_DIR, backup_name)
    with tarfile.open(backup_path, "w:gz") as tar:
        for folder in SOURCE_DIRS:
            if os.path.exists(folder):
                print(f"[OK] Archiving {folder}/")
                tar.add(folder, arcname=folder)
            else:
                print(f"[SKIP] Missing folder: {folder}")
    print(f"[OK] Brain backup complete -> {backup_path}")

# ========== Deep File Crawler ==========
def deep_file_crawl():
    import hashlib
    def hash_file(path, chunk_size=8192):
        try:
            hasher = hashlib.md5()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR: {e}"

    def crawl_directory(root_path, out_path):
        count = 0
        with open(out_path, 'w', encoding='utf-8') as out_file:
            for dirpath, _, filenames in os.walk(root_path):
                for file in filenames:
                    full_path = os.path.join(dirpath, file)
                    try:
                        stat = os.stat(full_path)
                        hashed = hash_file(full_path)
                        line = f"{full_path} | {stat.st_size} bytes | hash: {hashed}"
                    except Exception as e:
                        line = f"{full_path} | ERROR: {str(e)}"
                    out_file.write(line + "\n")
                    count += 1
                    if count % 100 == 0:
                        print(f"[OK] {count} files crawled...")
        print(f"[OK] Crawl complete. Total files: {count}")
        print(f"[OK] Full output saved to: {out_path}")

    BASE = "."
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_txt = f"neurostore_crawl_output_{timestamp}.txt"
    print(f"[OK] Starting deep crawl on: {BASE}")
    crawl_directory(BASE, output_txt)

# ========== Zip Project ==========
def zip_project():
    BASE = Path(".").resolve()
    zip_path = BASE.parent / f"{BASE.name}_project.zip"
    print(f"[OK] Zipping project to: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in BASE.rglob("*"):
            if file.is_file():
                zipf.write(file, arcname=file.relative_to(BASE))
    print("[OK] ZIP complete.")

# ========== Entrypoint ==========
if __name__ == "__main__":
    backup_neurostore()
    deep_file_crawl()
    zip_project()
# ========== symbol_seed_generator.py ==========
write_file(["symbol_seed_generator.py"], '''
import os
import yaml
import hashlib
from datetime import datetime

USE_LLM = False
MODEL_PATH = "models/mistral-7b-q4.gguf"
SEED_OUTPUT_DIR = "fragments/core/"
SEED_COUNT = 100

BASE_SEEDS = [
    "truth is important",
    "conflict creates learning",
    "change is constant",
    "observation precedes action",
    "emotion influences memory",
    "self seeks meaning",
    "logic guides belief",
    "doubt triggers inquiry",
    "energy becomes form",
    "ideas replicate",
    "something must stay_still so everything else can move"
]

def generate_id(content):
    return hashlib.sha256(content.encode()).hexdigest()[:12]

def to_fragment(statement):
    parts = statement.split()
    if len(parts) < 3:
        return None
    subj = parts[0]
    pred = parts[1]
    obj = "_".join(parts[2:])
    return {
        "id": generate_id(statement),
        "predicate": pred,
        "arguments": [subj, obj],
        "confidence": 1.0,
        "emotion": {
            "curiosity": 0.8,
            "certainty": 1.0
        },
        "tags": ["seed", "immutable", "core"],
        "immutable": True,
        "claim": statement,
        "timestamp": datetime.utcnow().isoformat()
    }

def save_fragment(fragment, output_dir):
    fname = f"frag_{fragment['id']}.yaml"
    path = os.path.join(output_dir, fname)
    with open(path, 'w') as f:
        yaml.dump(fragment, f)

def generate_symbolic_seeds():
    if not os.path.exists(SEED_OUTPUT_DIR):
        os.makedirs(SEED_OUTPUT_DIR)
    seed_statements = BASE_SEEDS[:SEED_COUNT]
    count = 0
    for stmt in seed_statements:
        frag = to_fragment(stmt)
        if frag:
            save_fragment(frag, SEED_OUTPUT_DIR)
            count += 1
    print(f"Generated {count} symbolic seed fragments in {SEED_OUTPUT_DIR}")

if __name__ == "__main__":
    generate_symbolic_seeds()
''')

# ========== token_agent.py ==========
write_file(["token_agent.py"], '''
import time
import random
import yaml
from pathlib import Path
from core.cortex_bus import send_message

FRAG_DIR = Path("fragments/core")

class TokenAgent:
    def __init__(self, agent_id="token_agent_01"):
        self.agent_id = agent_id
        self.frag_path = FRAG_DIR
        self.fragment_cache = []

    def load_fragments(self):
        files = list(self.frag_path.glob("*.yaml"))
        random.shuffle(files)
        for f in files:
            with open(f, 'r', encoding='utf-8') as file:
                try:
                    frag = yaml.safe_load(file)
                    if frag:
                        self.fragment_cache.append((f, frag))
                except yaml.YAMLError as e:
                    print(f"[{self.agent_id}] YAML error in {f.name}: {e}")

    def walk_fragment(self, path, frag):
        if 'claim' not in frag:
            return
        walk_log = {
            'fragment': path.name,
            'claim': frag['claim'],
            'tags': frag.get('tags', []),
            'confidence': frag.get('confidence', 0.5),
            'walk_time': time.time()
        }
        if random.random() < 0.2:
            walk_log['flag_mutation'] = True
        send_message({
            'from': self.agent_id,
            'type': 'walk_log',
            'payload': walk_log,
            'timestamp': int(time.time())
        })

    def run(self):
        self.load_fragments()
        for path, frag in self.fragment_cache:
            self.walk_fragment(path, frag)
            time.sleep(0.1)

if __name__ == "__main__":
    agent = TokenAgent()
    agent.run()
''')
# ========== backup_and_export.py ==========
write_file(["backup_and_export.py"], '''
import os
import tarfile
from datetime import datetime

EXPORT_DIR = os.path.expanduser("~/neurostore/backups")
SOURCE_DIRS = ["agents", "fragments", "logs", "meta", "runtime", "data"]

os.makedirs(EXPORT_DIR, exist_ok=True)
backup_name = f"neurostore_brain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
backup_path = os.path.join(EXPORT_DIR, backup_name)

with tarfile.open(backup_path, "w:gz") as tar:
    for folder in SOURCE_DIRS:
        if os.path.exists(folder):
            print(f"[+] Archiving {folder}/")
            tar.add(folder, arcname=folder)
        else:
            print(f"[-] Skipped missing folder: {folder}")

print(f"[OK] Brain backup complete -> {backup_path}")
''')

# ========== deep_file_crawler.py ==========
write_file(["deep_file_crawler.py"], '''
import os
import hashlib
from datetime import datetime

def hash_file(path, chunk_size=8192):
    try:
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def crawl_directory(root_path, out_path):
    count = 0
    with open(out_path, 'w') as out_file:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                try:
                    stat = os.stat(full_path)
                    hashed = hash_file(full_path)
                    line = f"{full_path} | {stat.st_size} bytes | hash: {hashed}"
                except Exception as e:
                    line = f"{full_path} | ERROR: {str(e)}"
                out_file.write(line + "\\n")
                count += 1
                if count % 100 == 0:
                    print(f"[+] {count} files crawled...")

    print(f"[OK] Crawl complete. Total files: {count}")
    print(f"[OK] Full output saved to: {out_path}")

if __name__ == "__main__":
    BASE = "."
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_txt = f"neurostore_crawl_output_{timestamp}.txt"
    print(f"[*] Starting deep crawl on: {BASE}")
    crawl_directory(BASE, output_txt)
''')

# ========== boot_wrapper.py ==========
write_file(["boot_wrapper.py"], '''
import subprocess
import os
import platform
import time
import psutil
from pathlib import Path

SCRIPTS = [
    "deep_system_scan.py",
    "auto_configurator.py",
    "path_optimizer.py",
    "fragment_teleporter.py",
    "run_logicshredder.py"
]

LOG_PATH = Path("logs/boot_times.log")
LOG_PATH.parent.mkdir(exist_ok=True)

def run_script(name, timings):
    if not Path(name).exists():
        print(f"[boot] ❌ Missing script: {name}")
        timings.append((name, "MISSING", "-", "-"))
        return False

    print(f"[boot] ▶ Running: {name}")
    start = time.time()
    proc = psutil.Popen(["python", name])

    peak_mem = 0
    cpu_percent = []

    try:
        while proc.is_running():
            mem = proc.memory_info().rss / (1024**2)
            peak_mem = max(peak_mem, mem)
            cpu = proc.cpu_percent(interval=0.1)
            cpu_percent.append(cpu)
    except Exception:
        pass

    end = time.time()
    duration = round(end - start, 2)
    avg_cpu = round(sum(cpu_percent) / len(cpu_percent), 1) if cpu_percent else 0

    print(f"[boot] ⏱ {name} finished in {duration}s | CPU: {avg_cpu}% | MEM: {int(peak_mem)}MB")
    timings.append((name, duration, avg_cpu, int(peak_mem)))
    return proc.returncode == 0

def log_timings(timings, total):
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"\\n=== BOOT TELEMETRY [{time.strftime('%Y-%m-%d %H:%M:%S')}] ===\\n")
        for name, dur, cpu, mem in timings:
            log.write(f" - {name}: {dur}s | CPU: {cpu}% | MEM: {mem}MB\\n")
        log.write(f"TOTAL BOOT TIME: {round(total, 2)} seconds\\n")

def main():
    print("🔧 LOGICSHREDDER SYSTEM BOOT STARTED")
    print(f"🧠 Platform: {platform.system()} | Python: {platform.python_version()}")
    print("==============================================\\n")

    start_total = time.time()
    timings = []

    for script in SCRIPTS:
        success = run_script(script, timings)
        if not success:
            print(f"[boot] 🛑 Boot aborted due to failure in {script}")
            break

    total_time = time.time() - start_total
    print(f"[OK] BOOT COMPLETE in {round(total_time, 2)} seconds.")
    log_timings(timings, total_time)

if __name__ == "__main__":
    main()
''')
# ========== nvme_memory_shim.py ==========
write_file(["nvme_memory_shim.py"], '''
import os
import time
import yaml
import psutil
from pathlib import Path
from shutil import disk_usage

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "system_config.yaml"
LOGIC_CACHE = BASE / "hotcache"

def detect_nvmes():
    nvmes = []
    fallback_mounts = ['C', 'D', 'E', 'F']
    for part in psutil.disk_partitions():
        label = part.device.lower()
        try:
            usage = disk_usage(part.mountpoint)
            is_nvme = any(x in label for x in ['nvme', 'ssd'])
            is_fallback = part.mountpoint.strip(':').upper() in fallback_mounts
            if is_nvme or is_fallback:
                nvmes.append({
                    'mount': part.mountpoint,
                    'fstype': part.fstype,
                    'free_gb': round(usage.free / 1e9, 2),
                    'total_gb': round(usage.total / 1e9, 2)
                })
        except Exception:
            continue
    print(f"[shim] Detected {len(nvmes)} logic-capable drive(s): {[n['mount'] for n in nvmes]}")
    return sorted(nvmes, key=lambda d: d['free_gb'], reverse=True)

def assign_as_logic_ram(nvmes):
    logic_zones = {}
    for i, nvme in enumerate(nvmes[:4]):
        zone = f"ram_shard_{i+1}"
        path = Path(nvme['mount']) / "logicshred_cache"
        path.mkdir(exist_ok=True)
        logic_zones[zone] = str(path)
    return logic_zones

def update_config(zones):
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    config['logic_ram'] = zones
    config['hotcache_path'] = str(LOGIC_CACHE)
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config, f)
    print(f"[OK] Config updated with NVMe logic cache: {list(zones.values())}")

if __name__ == "__main__":
    LOGIC_CACHE.mkdir(exist_ok=True)
    print("[INFO] Detecting NVMe drives and logic RAM mounts...")
    drives = detect_nvmes()
    if not drives:
        print("[WARN] No NVMe or fallback drives detected. System unchanged.")
    else:
        zones = assign_as_logic_ram(drives)
        update_config(zones)
''')

# ========== fragment_teleporter.py ==========
write_file(["fragment_teleporter.py"], '''
import shutil
from pathlib import Path

CORE_DIR = Path("fragments/core")
TARGETS = [Path("fragments/node1"), Path("fragments/node2")]
TRANSFER_LOG = Path("logs/teleport_log.txt")
TRANSFER_LOG.parent.mkdir(parents=True, exist_ok=True)

for target in TARGETS:
    target.mkdir(parents=True, exist_ok=True)

class FragmentTeleporter:
    def __init__(self, limit=5):
        self.limit = limit

    def select_fragments(self):
        frags = list(CORE_DIR.glob("*.yaml"))
        return frags[:self.limit] if frags else []

    def teleport(self):
        selections = self.select_fragments()
        for i, frag_path in enumerate(selections):
            target = TARGETS[i % len(TARGETS)] / frag_path.name
            shutil.move(str(frag_path), target)
            with open(TRANSFER_LOG, 'a') as log:
                log.write(f"[TELEPORTED] {frag_path.name} -> {target}\\n")
            print(f"[Teleporter] {frag_path.name} -> {target}")

if __name__ == "__main__":
    teleporter = FragmentTeleporter(limit=10)
    teleporter.teleport()
''')

# ========== context_activator.py ==========
write_file(["context_activator.py"], '''
import yaml
from pathlib import Path

FRAGMENTS_DIR = Path("fragments/core")
ACTIVATION_LOG = Path("logs/context_activation.log")
ACTIVATION_LOG.parent.mkdir(parents=True, exist_ok=True)

class ContextActivator:
    def __init__(self, activation_threshold=0.75):
        self.threshold = activation_threshold

    def scan_fragments(self):
        activated = []
        for frag_file in FRAGMENTS_DIR.glob("*.yaml"):
            try:
                with open(frag_file, 'r') as f:
                    frag = yaml.safe_load(f)
                if frag.get("confidence", 0.5) >= self.threshold:
                    activated.append(frag)
            except Exception as e:
                print(f"Error reading {frag_file.name}: {e}")
        return activated

    def log_activations(self, activations):
        with open(ACTIVATION_LOG, 'a') as log:
            for frag in activations:
                log.write(f"[ACTIVATED] {frag['id']} :: {frag.get('claim', '???')}\\n")
        print(f"[ContextActivator] {len(activations)} fragment(s) activated.")

    def run(self):
        active = self.scan_fragments()
        self.log_activations(active)

if __name__ == "__main__":
    ctx = ContextActivator()
    ctx.run()
''')

# ========== subcon_layer_mapper.py ==========
write_file(["subcon_layer_mapper.py"], '''
import os
import yaml
from pathlib import Path

LAYER_MAP_PATH = Path("subcon_map.yaml")
FRAGMENTS_DIR = Path("fragments/core")
OUTPUT_PATH = Path("meta/subcon_layer_cache.yaml")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

class SubconLayerMapper:
    def __init__(self):
        self.layer_map = self.load_map()

    def load_map(self):
        if not LAYER_MAP_PATH.exists():
            print("[Mapper] No layer map found. Returning empty.")
            return {}
        with open(LAYER_MAP_PATH, 'r') as f:
            return yaml.safe_load(f)

    def extract_links(self):
        results = {}
        for file in FRAGMENTS_DIR.glob("*.yaml"):
            try:
                with open(file, 'r') as f:
                    frag = yaml.safe_load(f)
                tags = frag.get("tags", [])
                for tag in tags:
                    if tag in self.layer_map:
                        results.setdefault(tag, []).append(frag['id'])
            except Exception as e:
                print(f"[Mapper] Failed to read {file.name}: {e}")
        return results

    def save_cache(self, data):
        with open(OUTPUT_PATH, 'w') as out:
            yaml.dump(data, out)
        print(f"[Mapper] Saved subcon layer associations -> {OUTPUT_PATH}")

    def run(self):
        links = self.extract_links()
        self.save_cache(links)

if __name__ == "__main__":
    mapper = SubconLayerMapper()
    mapper.run()
''')
# ========== validator.py ==========
write_file(["validator.py"], '''
import os
import time
from pathlib import Path
import yaml
from core.utils import load_yaml, hash_string, validate_fragment
from core.cortex_bus import send_message

CORE_DIR = Path("fragments/core")
OVERFLOW_DIR = Path("fragments/overflow")
OVERFLOW_DIR.mkdir(parents=True, exist_ok=True)

class Validator:
    def __init__(self, agent_id="validator_01"):
        self.agent_id = agent_id
        self.frags = {}

    def load_core_beliefs(self):
        for path in CORE_DIR.glob("*.yaml"):
            frag = load_yaml(path, validate_schema=validate_fragment)
            if frag:
                claim_hash = hash_string(frag['claim'])
                self.frags[claim_hash] = (path, frag)

    def contradicts(self, a, b):
        return a.lower().strip() == f"not {b.lower().strip()}"

    def run_validation(self):
        for hash_a, (path_a, frag_a) in self.frags.items():
            for hash_b, (path_b, frag_b) in self.frags.items():
                if hash_a == hash_b:
                    continue
                if self.contradicts(frag_a['claim'], frag_b['claim']):
                    contradiction_id = f"{hash_a[:6]}_{hash_b[:6]}"
                    filename = f"contradiction_{contradiction_id}.yaml"
                    contradiction_path = OVERFLOW_DIR / filename
                    if not contradiction_path.exists():
                        contradiction = {
                            'source_1': frag_a['claim'],
                            'source_2': frag_b['claim'],
                            'path_1': str(path_a),
                            'path_2': str(path_b),
                            'detected_by': self.agent_id,
                            'timestamp': int(time.time())
                        }
                        with open(contradiction_path, 'w') as out:
                            yaml.dump(contradiction, out)
                        send_message({
                            'from': self.agent_id,
                            'type': 'contradiction_found',
                            'payload': {
                                'claim_1': frag_a['claim'],
                                'claim_2': frag_b['claim'],
                                'paths': [str(path_a), str(path_b)]
                            },
                            'timestamp': int(time.time())
                        })

    def run(self):
        self.load_core_beliefs()
        self.run_validation()

if __name__ == "__main__":
    Validator().run()
''')

# ========== inject_profiler.py ==========
write_file(["inject_profiler.py"], '''
import time
import psutil

class InjectProfiler:
    def __init__(self, label="logic_injection"):
        self.label = label
        self.snapshots = []

    def snapshot(self):
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=0.1)
        self.snapshots.append((time.time(), mem, cpu))

    def report(self):
        print(f"[Profiler:{self.label}] Total snapshots: {len(self.snapshots)}")
        for t, mem, cpu in self.snapshots:
            print(f" - {round(t, 2)}s :: MEM {mem}% | CPU {cpu}%")

if __name__ == "__main__":
    p = InjectProfiler()
    for _ in range(5):
        p.snapshot()
        time.sleep(1)
    p.report()
''')

# ========== async_swarm_launcher.py ==========
write_file(["async_swarm_launcher.py"], '''
import asyncio
import subprocess

TASKS = [
    "fragment_decay_engine.py",
    "dreamwalker.py",
    "validator.py",
    "mutation_engine.py"
]

async def run_script(name):
    proc = await asyncio.create_subprocess_exec("python", name)
    await proc.wait()

async def main():
    coros = [run_script(task) for task in TASKS]
    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(main())
''')

# ========== requirements_installer.py ==========
write_file(["requirements_installer.py"], '''
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
''')
