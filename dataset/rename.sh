#!/bin/bash

# Counter starts at 1
counter=1

# Loop through all PDF files in the current directory
for file in *.pdf; do
  # Check if the file exists
  if [[ -f "$file" ]]; then
    # Generate new filename with the counter
    new_name="sal_${counter}.pdf"

    # Rename the file
    mv "$file" "$new_name"

    # Increment the counter
    ((counter++))
  fi
done

echo "Renaming complete: $(($counter - 1)) files renamed."

