#!/bin/bash
# DINNER.oot & RULES.oot 1.7 Pre-Commit Enforcement Hook

STAGED_OO=$(git diff --cached --name-only --diff-filter=ACM | grep '\.oo$' || true)

if [ -z "$STAGED_OO" ]; then
    exit 0
fi

FAILS=0

for FILE in $STAGED_OO; do
    if [ ! -f "$FILE" ]; then
        continue
    fi
    
    # Skip intentional stress fixture
    if [[ "$FILE" == *"fixtures/b8_repro.oo" ]]; then
        continue
    fi

    # 1. Check line limit (RULES.oot 1.7)
    LINES=$(wc -l < "$FILE")
    if [ "$LINES" -gt 256 ]; then
        echo "❌ [DINNER ERROR] $FILE: $LINES lines (exceeds 256 line limit)"
        FAILS=$((FAILS + 1))
    fi

    # 2. Check Academy Header elements
    HEADER=$(head -n 25 "$FILE")
    if ! echo "$HEADER" | grep -q "^// # "; then
        echo "❌ [DINNER ERROR] $FILE: missing '// # <Title>'"
        FAILS=$((FAILS + 1))
    fi
    if ! echo "$HEADER" | grep -q "^// Logline:"; then
        echo "❌ [DINNER ERROR] $FILE: missing '// Logline:'"
        FAILS=$((FAILS + 1))
    fi
    
    # Check Setup and Beats for source files (non-fixtures)
    if [[ "$FILE" != *"fixtures/"* ]] && [[ "$FILE" != *"bootstrap/"* ]]; then
        if ! echo "$HEADER" | grep -q "^// Setup:"; then
            echo "❌ [DINNER ERROR] $FILE: missing '// Setup:'"
            FAILS=$((FAILS + 1))
        fi
        if ! echo "$HEADER" | grep -q "^// Beats:"; then
            echo "❌ [DINNER ERROR] $FILE: missing '// Beats:'"
            FAILS=$((FAILS + 1))
        fi
    fi
done

if [ "$FAILS" -gt 0 ]; then
    echo "⛔ Pre-commit rejected: $FAILS DINNER.oot violation(s) found."
    echo "Please fix the header and line limit constraints before committing."
    exit 1
fi

exit 0
