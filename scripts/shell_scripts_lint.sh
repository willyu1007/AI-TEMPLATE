#!/bin/bash
# Shell Scripts Linter - Validates shell scripts quality
#
# Purpose:
# - Check for proper shebang
# - Verify set -e (exit on error)
# - Check for undefined variables (set -u recommended)
# - Detect common issues
#
# Usage:
#     bash scripts/shell_scripts_lint.sh
#     make shell_scripts_lint

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

errors=0
warnings=0
checked=0

echo "🔍 Checking shell scripts..."

# Find all .sh files in scripts/
while IFS= read -r -d '' script_file; do
    ((checked++))
    filename=$(basename "$script_file")
    file_errors=()
    file_warnings=()
    
    # Check shebang
    first_line=$(head -n 1 "$script_file")
    if [[ ! "$first_line" =~ ^#!/bin/(bash|sh) ]]; then
        file_warnings+=("Missing proper shebang (#!/bin/bash or #!/bin/sh)")
    fi
    
    # Check for 'set -e' (exit on error)
    if ! grep -q "set -e" "$script_file"; then
        file_warnings+=("Consider adding 'set -e' to exit on error")
    fi
    
    # Check for 'set -u' (exit on undefined variable)
    if ! grep -q "set -u" "$script_file"; then
        file_warnings+=("Consider adding 'set -u' to catch undefined variables")
    fi
    
    # Check for dangerous practices
    if grep -q 'rm -rf \$' "$script_file"; then
        file_errors+=("Dangerous: 'rm -rf' with variable - may delete unintended files")
    fi
    
    # Check for unquoted variables (common mistake)
    if grep -E '\$[A-Z_][A-Z0-9_]*[^"]' "$script_file" | grep -v '^\s*#' > /dev/null 2>&1; then
        file_warnings+=("Unquoted variables detected - may cause issues with spaces")
    fi
    
    # Check for command existence before use
    # (e.g., using git without checking if it exists)
    if grep -q 'git ' "$script_file"; then
        if ! grep -q 'command -v git' "$script_file" && ! grep -q 'which git' "$script_file"; then
            file_warnings+=("Using 'git' without checking if command exists")
        fi
    fi
    
    # Report file issues
    if [ ${#file_errors[@]} -gt 0 ]; then
        echo ""
        echo "  $filename:"
        for error in "${file_errors[@]}"; do
            echo "    ❌ $error"
            ((errors++))
        done
    fi
    
    if [ ${#file_warnings[@]} -gt 0 ]; then
        if [ ${#file_errors[@]} -eq 0 ]; then
            echo ""
            echo "  $filename:"
        fi
        for warning in "${file_warnings[@]}"; do
            echo "    ⚠️  $warning"
            ((warnings++))
        done
    fi
    
done < <(find "$SCRIPT_DIR" -maxdepth 1 -name "*.sh" -type f -print0)

echo ""

if [ $errors -gt 0 ]; then
    echo "❌ Shell scripts lint failed with $errors error(s)"
    exit 1
elif [ $warnings -gt 0 ]; then
    echo "⚠️  Shell scripts lint passed with $warnings warning(s) ($checked files checked)"
    exit 0
else
    echo "✅ Shell scripts lint passed ($checked files checked)"
    exit 0
fi

