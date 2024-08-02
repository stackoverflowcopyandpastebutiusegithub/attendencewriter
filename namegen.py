import hashlib
import json
import os

def get_digest(file_path):
    try:
        h = hashlib.sha256()
        with open(file_path, 'rb') as file:
            while True:
                # Read in chunks to avoid memory issues
                chunk = file.read(h.block_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_output_file_name(counter):
    output_file_name = f"output({counter}).sha256"
    return output_file_name

def main():
    json_file_path = 'your_json_file.json'
    sha256_hash = get_digest(json_file_path)

    if sha256_hash:
        counter = 1
        output_file_name = get_output_file_name(counter)
        while os.path.exists(output_file_name):
            counter += 1
            output_file_name = get_output_file_name(counter)

        with open(output_file_name, 'w') as sha256_file:
            sha256_file.write(sha256_hash)

        print(f"SHA-256 hash written to '{output_file_name}'")

if __name__ == "__main__":
    main()