import mmap
import os
import re
import argparse

def binary_search_log(file_path, target_date):
    with open(file_path, 'r') as file:
        mapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        low, high = 0, len(mapped_file)
        while low < high:
            mid = (low + high) // 2
            mapped_file.seek(mid)
            mapped_file.readline()  # Skip incomplete line
            line = mapped_file.readline().decode()
            if not line:
                high = mid
                continue
            timestamp = line[:10]
            if timestamp < target_date:
                low = mid + 1
            else:
                high = mid
        return low  # Approximate starting position

def extract_logs(file_path, target_date):
    start_pos = binary_search_log(file_path, target_date)
    results = []
    with open(file_path, 'r') as file:
        file.seek(start_pos)
        for line in file:
            if line.startswith(target_date):
                results.append(line.strip())
            elif results:
                break  # Stop once we move to the next date
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Path to the log file')
    parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format')
    args = parser.parse_args()
    logs = extract_logs(args.file_path, args.date)
    for log in logs:
        print(log)

if __name__ == '__main__':
    main()
