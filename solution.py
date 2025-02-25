import os
import argparse
import heapq

def extract_logs(file_path, target_date):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(target_date):
                results.append(line.strip())
    return results

def optimized_log_search(file_path, target_date):
    chunk_size = 1024 * 1024  # 1MB chunks
    with open(file_path, 'r') as file:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        position = 0
        while position < file_size:
            file.seek(position)
            lines = file.read(chunk_size).splitlines()
            for line in lines:
                if line.startswith(target_date):
                    yield line.strip()
            position += chunk_size

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Path to the log file')
    parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format')
    args = parser.parse_args()
    
    logs = list(optimized_log_search(args.file_path, args.date))
    for log in heapq.nsmallest(len(logs), logs):  # Maintain order
        print(log)

if __name__ == '__main__':
    main()
