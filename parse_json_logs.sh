#!/bin/bash

# Parse JSON log file and find all lines containing ERROR
# Usage: ./parse_json_logs.sh <log_file_path> [output_file]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <log_file_path> [output_file]"
    exit 1
fi

LOG_FILE="$1"
OUTPUT_FILE="$2"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found."
    exit 1
fi

# Count and display ERROR lines
echo "Parsing $LOG_FILE for ERROR entries..."
echo ""

ERROR_COUNT=0
TEMP_OUTPUT=$(mktemp)

while IFS= read -r line; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi
    
    # Check if line contains ERROR (case-insensitive)
    if echo "$line" | grep -qi "ERROR"; then
        ((ERROR_COUNT++))
        echo "Line $ERROR_COUNT: $line" >> "$TEMP_OUTPUT"
    fi
done < "$LOG_FILE"

# Output results
if [ $ERROR_COUNT -gt 0 ]; then
    echo "Found $ERROR_COUNT ERROR entries:"
    echo ""
    cat "$TEMP_OUTPUT"
    
    # Save to file if output file specified
    if [ -n "$OUTPUT_FILE" ]; then
        cp "$TEMP_OUTPUT" "$OUTPUT_FILE"
        echo ""
        echo "Results saved to $OUTPUT_FILE"
    fi
else
    echo "No ERROR entries found."
fi

# Clean up temp file
rm "$TEMP_OUTPUT"
