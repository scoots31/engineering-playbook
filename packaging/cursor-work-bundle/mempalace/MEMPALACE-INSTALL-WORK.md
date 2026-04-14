# MemPalace on a work laptop (no GitHub clone required)

MemPalace is typically installed with **Python**. On a locked-down machine you may only have **pip** / **pipx** from internal mirrors—use whatever your IT policy allows.

## 1. Create a dedicated venv (recommended)

```bash
python3 -m venv ~/Apps/mempalace-venv
source ~/Apps/mempalace-venv/bin/activate
pip install mempalace
which mempalace
```

Use the path printed by `which mempalace` as **`{{MEMPALACE_CLI}}`** in Cursor User rules (absolute path, e.g. `/Users/you/Apps/mempalace-venv/bin/mempalace`).

## 2. Or pipx (if available)

```bash
pipx install mempalace
which mempalace
```

## 3. First run

```bash
mempalace --help
mempalace status
```

Data usually lives under `~/.mempalace/` after first use. See MemPalace’s own docs if your version differs.

## 4. If pip cannot reach the internet

- Ask IT for an **approved** Python package mirror or a **pre-built wheel** on an internal file share.
- Worst case: install MemPalace on a **permitted** machine, then copy **only** the venv folder and `~/.mempalace` via approved transfer (check policy before copying dot-directories).

## 5. Cursor rules

After `mempalace` works in Terminal, paste its **absolute path** into the MemPalace section of `templates/cursor-user-rules-WORK-template.md` (replace `{{MEMPALACE_CLI}}`).
