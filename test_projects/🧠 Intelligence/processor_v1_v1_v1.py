# Data processor with missing docstrings and type hints
import csv
import json


def load_data(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def process_data(data):
    processed = []
    for item in data:
        if item["status"] == "active":
            processed.append(item)
    return processed


def save_to_csv(data, output_file):
    with open(output_file, "w", newline="") as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)


def main():
    try:
        data = load_data("input.json")
        processed = process_data(data)
        save_to_csv(processed, "output.csv")
        print("Data processing complete!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
