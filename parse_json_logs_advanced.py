import json
import sys
from pathlib import Path

def find_error_lines(log_file_path, fields=None):
    """
    Parse a JSON log file and find all lines containing ERROR.
    
    Args:
        log_file_path: Path to the JSON log file
        fields: Optional list of specific fields to search (e.g., ['level', 'message'])
        
    Returns:
        List of error entries with metadata
    """
    error_lines = []
    
    try:
        with open(log_file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    log_entry = json.loads(line)
                    
                    # If specific fields provided, check only those
                    if fields:
                        search_values = [str(log_entry.get(field, '')) for field in fields]
                    else:
                        search_values = [str(v) for v in log_entry.values()]
                    
                    # Check for ERROR
                    if any('ERROR' in value.upper() for value in search_values):
                        error_lines.append({
                            'line_number': line_num,
                            'entry': log_entry
                        })
                except json.JSONDecodeError:
                    if 'ERROR' in line.upper():
                        error_lines.append({
                            'line_number': line_num,
                            'entry': line,
                            'parse_error': True
                        })
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return []
    
    return error_lines


def export_results(errors, output_file=None):
    """Export error lines to file or stdout"""
    output = json.dumps(errors, indent=2)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"Results saved to {output_file}")
    else:
        print(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_json_logs_advanced.py <log_file> [output_file]")
        sys.exit(1)
    
    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    errors = find_error_lines(log_file)
    print(f"Found {len(errors)} ERROR entries")
    export_results(errors, output_file)
