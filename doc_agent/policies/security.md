---
audience: ai
language: en
version: summary
purpose: Quick security guidelines for AI agents
full_version: /doc/policies/security_details.md
---

# Security Guidelines - Quick Reference

> **For AI Agents** - Essential security rules (~120 lines)  
> **Full Guide**: [security_details.md](security_details.md) (537 lines, for humans)

---

## Core Principles (4)

### 1. Secrets Management
- ❌ **NEVER commit secrets** to repository
- ✅ Use environment variables for sensitive data
- ✅ Use secret management service (production)
- ✅ Rotate secrets regularly (every 90 days)

### 2. Least Privilege
- ✅ Grant minimum necessary permissions
- ✅ Scope access to specific paths/modules
- ❌ No wildcard permissions
- ✅ Review permissions quarterly

### 3. Defense in Depth
- ✅ Multiple security layers
- ✅ Input validation + output encoding
- ✅ Authentication + authorization
- ✅ Audit logging enabled

### 4. Fail Secure
- ✅ Errors deny by default
- ✅ Timeouts deny by default
- ❌ Never expose internal errors to users
- ✅ Log security events

---

## Critical Rules (10)

### Configuration
1. ❌ **BLOCKED**: Never edit `config/prod.yaml` directly
2. ⚠️ **WARNING**: Staging config changes need confirmation
3. ✅ **ALLOWED**: Dev config can be freely edited

### Secrets
4. ❌ **BLOCKED**: No hardcoded secrets (API keys, passwords, tokens)
5. ✅ **REQUIRED**: Use environment variables or secret service
6. ✅ **REQUIRED**: Add secret patterns to `.gitignore`

### Database
7. ✅ **REQUIRED**: All migrations need rollback scripts (down.sql)
8. ⚠️ **WARNING**: DDL changes need human review before execution
9. ❌ **BLOCKED**: No direct production database access by AI

### Code
10. ✅ **REQUIRED**: All user input must be validated and sanitized

---

## Quick Checks

### Before Commit
```bash
# Check for secrets
make secret_scan

# Check for security issues
make observability_check

# Full check
make dev_check
```

### Scan Patterns (Detected by secret_scan)
- API keys: `api_key = "xxx"`
- Passwords: `password = "xxx"`
- Tokens: `token = "xxx"`
- Connection strings: `postgres://user:pass@host`
- Private keys: `-----BEGIN PRIVATE KEY-----`

---

## Input Validation

### Required for ALL User Inputs

```python
# Example
def process_user_input(data: dict) -> dict:
    # 1. Validate type
    if not isinstance(data, dict):
        raise ValueError("Invalid input type")
    
    # 2. Validate required fields
    required = ["field1", "field2"]
    if not all(k in data for k in required):
        raise ValueError("Missing required fields")
    
    # 3. Sanitize strings
    safe_data = {k: sanitize(v) for k, v in data.items()}
    
    # 4. Validate constraints
    validate_constraints(safe_data)
    
    return safe_data
```

---

## Common Vulnerabilities (Prevent)

### 1. SQL Injection
```python
# ❌ BAD - String concatenation
query = f"SELECT * FROM users WHERE name = '{user_name}'"

# ✅ GOOD - Parameterized query
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_name,))
```

### 2. Path Traversal
```python
# ❌ BAD - Unchecked path
file_path = f"/data/{user_file}"

# ✅ GOOD - Validate path
import os
safe_path = os.path.join("/data", os.path.basename(user_file))
```

### 3. Command Injection
```python
# ❌ BAD - Shell=True with user input
os.system(f"ls {user_dir}")

# ✅ GOOD - List arguments, no shell
subprocess.run(["ls", user_dir])
```

---

## Security Checklist

### For Every Change

- [ ] No secrets committed (`make secret_scan`)
- [ ] All user inputs validated
- [ ] No SQL injection vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] Error messages don't expose internals
- [ ] Security-sensitive operations logged
- [ ] Config changes reviewed (if production)

---

## Incident Response

### If Secret Leaked

1. **IMMEDIATE**: Revoke the compromised secret
2. **Urgent**: Rotate to new secret
3. **Required**: Check for unauthorized access
4. **Required**: Update `.gitignore` to prevent recurrence
5. **Required**: Use `git filter-branch` or BFG to remove from history

```bash
# Remove secret from history (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all
```

---

## Related Commands

```bash
make secret_scan              # Scan for secrets
make observability_check      # Check logging/monitoring
make health_check             # Full security review included
```

---

## Related Docs

- **Full Guide**: [security_details.md](security_details.md) (537 lines)
- **Safety Rules**: [safety.md](safety.md) (233 lines)
- **Quality Standards**: [quality_standards.md](quality_standards.md) (402 lines)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Lines**: ~120

