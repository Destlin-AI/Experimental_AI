
import os
import yaml
import random

def create_mesh(base_dir="F:/logic_core", count=50):
    os.makedirs(base_dir, exist_ok=True)

    for i in range(1, count + 1):
        part_name = f"p_{i:03}"
        part_path = os.path.join(base_dir, part_name)
        os.makedirs(part_path, exist_ok=True)

        # Drop a config file with symbolic parameters
        config = {
            "id": part_name,
            "emotion_bias": random.choice(["neutral", "anger", "joy", "curiosity", "melancholy"]),
            "decay_rate": round(random.uniform(0.93, 0.99), 3),
            "walk_style": random.choice(["conservative", "aggressive", "balanced"]),
            "linked_neighbors": [],
        }

        # Mesh connection simulation — link to 2 random other nodes
        available = [f"p_{j:03}" for j in range(1, count + 1) if j != i]
        config["linked_neighbors"] = random.sample(available, k=2)

        config_path = os.path.join(part_path, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        print(f"INFO {part_name} initialized with links -> {config['linked_neighbors']}")

if __name__ == "__main__":
    create_mesh()
