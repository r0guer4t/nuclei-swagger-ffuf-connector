#!/usr/bin/bash

# Configurations
URLS_FILE="ffufFUZZ.txt"  # File containing the list of URLs with methods
WORDLIST1="/home/[USER]/SecLists/Fuzzing/XML-FUZZ.txt"  # First wordlist
WORDLIST2="/home/[USER]/SecLists/Fuzzing/LDAP.Fuzzing.txt"  # Second wordlist
OUTPUT_DIR="./ffuf_results"  # Directory to store results


mkdir -p "$OUTPUT_DIR"

sanitize_filename() {
  
    echo "$1" | sed 's/[^a-zA-Z0-9]/_/g'
}

run_ffuf() {
    local method="$1"
    local url="$2"

    [[ -z "$url" ]] && return

    local sanitized_url
    sanitized_url=$(sanitize_filename "$url")
    local output_file="$OUTPUT_DIR/${sanitized_url}_ffuf.json"
    if [[ "$method" == "POST" ]]; then
        ffuf -u "$url" \
             -w "$WORDLIST1:FUZZ" \
             -w "$WORDLIST2:SECOND" \
             -mode clusterbomb \
             -rate 100 \
             -fc 401,502,403,405 \
             -o "$output_file" \
             -of json \
             -X "$method" \
             -d "SECOND"
    else
        ffuf -u "$url" \
             -w "$WORDLIST1:FUZZ" \
             -w "$WORDLIST2:SECOND" \
             -mode clusterbomb \
             -rate 100 \
             -fc 401,502,403,405 \
             -o "$output_file" \
             -of json \
             -X "$method" \
             -d "SECOND"
    fi

    if [[ $? -eq 0 ]]; then
        echo "Results for $url saved to $output_file"
    else
        echo "Error running ffuf for $url"
    fi
}

main() {
    
    if [[ ! -f "$URLS_FILE" ]]; then
        echo "URLs file '$URLS_FILE' does not exist."
        return
    fi

    
    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ -z "$line" ]] && continue

        
        method=$(echo "$line" | awk '{print $1}')
        url=$(echo "$line" | awk '{print $2}')
       
        if [[ -z "$method" || -z "$url" ]]; then
            echo "Invalid line format: $line"
            continue
        fi

        run_ffuf "$method" "$url"
    done < "$URLS_FILE"

    echo "All URLs processed. Results are in the '$OUTPUT_DIR' directory."
}

main