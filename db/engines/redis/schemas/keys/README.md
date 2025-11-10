# Redis Key Specifications

Use this folder to describe Redis key spaces, structures, and lifecycle policies.  
Each file should capture:

1. **Key pattern** (`cache:<module>:<id>`).  
2. **Data type** (String, Hash, List, Set, ZSet, Stream).  
3. **Field schema** (for Hash/JSON payloads).  
4. **TTL / refresh policy**.  
5. **Owner module** and escalation contacts.  
6. **References** to consuming services or docs.

Example template:

```yaml
key: cache:recommendation:<user_id>
type: hash
ttl_seconds: 3600
fields:
  score: float
  generated_at: iso8601
owner: modules/recommendation
notes:
  - "Regenerated after new interaction events."
  - "Purge with BRPOP on queue:recommendation:refresh"
```

Keep key specs under version control and update them whenever structure or TTL changes.


