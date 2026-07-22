#!/bin/bash

# Advanced JSON log parser - finds ERROR lines and exports to JSON
# Usage: ./parse_json_logs_advanced.sh <log_file_path> [output_file] [field1,field2,...]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <log_file_path> [output_file] [fields_to_search]"
    echo "Example: $0 app.log errors.json 'level,message'"
    exit 1
fi

LOG_FILE="$1"
OUTPUT_FILE="${2:-}"
FIELDS="${3:-}"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found."
    exit 1
fi

echo "Parsing $LOG_FILE for ERROR entries..."
echo ""

# Create temporary JSON array
TEMP_JSON=$(mktemp)
echo "[" > "$TEMP_JSON"

ERROR_COUNT=0
FIRST_ENTRY=true

while IFS= read -r line; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi
    
    # Check if line contains ERROR
    if echo "$line" | grep -qi "ERROR"; then
        # Add comma before new entry (except for first)
        if [ "$FIRST_ENTRY" = false ]; then
            echo "," >> "$TEMP_JSON"
        fi
        FIRST_ENTRY=false
        
        # Try to parse as JSON, otherwise treat as string
        if echo "$line" | jq . > /dev/null 2>&1; then
            echo "  {" >> "$TEMP_JSON"
            echo "    \"line_number\": $((++ERROR_COUNT))," >> "$TEMP_JSON"
            echo "    \"entry\": $line" >> "$TEMP_JSON"
            echo "  }" >> "$TEMP_JSON"
        else
            echo "  {" >> "$TEMP_JSON"
            echo "    \"line_number\": $((++ERROR_COUNT))," >> "$TEMP_JSON"
            echo "    \"entry\": \"$line\"" >> "$TEMP_JSON"
            echo "  }" >> "$TEMP_JSON"
        fi
    fi
done < "$LOG_FILE"

echo "]" >> "$TEMP_JSON"

# Display results
echo "Found $ERROR_COUNT ERROR entries:"
echo ""
cat "$TEMP_JSON" | jq '.' 2>/dev/null || cat "$TEMP_JSON"

# Save to file if output file specified
if [ -n "$OUTPUT_FILE" ]; then
    cat "$TEMP_JSON" > "$OUTPUT_FILE"
    echo ""
    echo "Results saved to $OUTPUT_FILE"
fi

# Clean up temp file
rm "$TEMP_JSON"
