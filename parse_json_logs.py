import json
import sys

def find_error_lines(log_file_path):
    """
    Parse a JSON log file and find all lines containing ERROR.
    
    Args:
        log_file_path: Path to the JSON log file
        
    Returns:
        List of error entries
    """
    error_lines = []
    
    try:
        with open(log_file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse JSON line
                    log_entry = json.loads(line)
                    
                    # Check if ERROR is in any field
                    if any('ERROR' in str(value).upper() for value in log_entry.values()):
                        error_lines.append({
                            'line_number': line_num,
                            'entry': log_entry
                        })
                except json.JSONDecodeError:
                    # If not valid JSON, check raw text for ERROR
                    if 'ERROR' in line.upper():
                        error_lines.append({
                            'line_number': line_num,
                            'entry': line
                        })
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return []
    
    return error_lines


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_json_logs.py <log_file_path>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    errors = find_error_lines(log_file)
    
    if errors:
        print(f"Found {len(errors)} ERROR entries:\n")
        for error in errors:
            print(f"Line {error['line_number']}: {json.dumps(error['entry'], indent=2)}")
    else:
        print("No ERROR entries found.")


if __name__ == "__main__":
    main()
