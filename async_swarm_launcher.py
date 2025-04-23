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
