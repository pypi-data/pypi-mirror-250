# Partial-sh

## Examples

Create `data.jsonl` [JSON Lines](https://jsonlines.org/) file:

```json
cat << EOF > data.jsonl
{"name":"John Doe","date_of_birth":"1980-01-01", "address": "123 Main St"}
{"name":"Jane Smith","date_of_birth":"1990-02-15", "address": "456 Main St"}
{"name":"Jay Neal","date_of_birth":"1993-07-27", "address": "42 Main 94111 St"}
{"name":"Lisa Ray","date_of_birth":"1985-03-03", "address": "789 Elm St"}
EOF
```

Transform the data:

```bash
cat data.jsonl | pt -i "Split firstname and lastname" -i "remove the address"
```
