import os

def generate_secrets():
    env_file = ".env"
    secrets_file = os.path.join("core", "secrets.py")

    if not os.path.exists(env_file):
        print(f"Error: {env_file} not found")
        return

    master_key = None
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("MASTER_KEY="):
                master_key = line.split("=", 1)[1].strip()
                break

    if not master_key:
        print("Error: MASTER_KEY not found in .env")
        return

    with open(secrets_file, "w") as f:
        f.write("AUTO-GENERATED FILE")
        f.write(f"MASTER_KEY = '{master_key}'\n")

    print(f"Successfully generated {secrets_file}")

if __name__ == "__main__":
    generate_secrets()