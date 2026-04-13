# Merging into `.cursor/hooks.json`

Add the `beforeShellExecution` entry below into your existing `hooks` object (merge with other events). If the file is new, use the full skeleton:

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": ".cursor/hooks/guard-destructive.sh",
        "failClosed": false
      }
    ]
  }
}
```

**Project layout:** place `guard-destructive.sh` in `.cursor/hooks/` and run `chmod +x .cursor/hooks/guard-destructive.sh`.

Tighten later with a `matcher` if you only want certain commands checked (see Cursor hook docs).
