"""Writing the app's sidecar JSON files: `settings.json`, `groups.json`,
`account.json`, `invites.json`, `write_links.json`, a made pack's
`theme.json`.

One function, because it was seven copies of the same three lines and one
of them had drifted. Four of the seven wrote `json.dumps(data, indent=2)`
without `ensure_ascii=False`, and those four are the ones carrying names
people typed: an account's `display_name` and a write link's `label` were
stored as `Am\\u00e9lie No\\u00eblle` while the same person's group name,
written by `groups.py`, stayed `Amélie Noëlle`. Nothing broke — Python
reads both back identically — but "plain text, readable long after this
app is gone" is the promise the whole storage design exists to keep, and
escape sequences are not what a family should find when they open their
own files.

A leaf on purpose: it imports nothing from the rest of the app, so
`settings.py` — which every request reads, and which keeps itself free of
app imports for that reason — can use it too.
"""

import json
import os
from pathlib import Path


def write_json(path, data) -> None:
    """Write `data` as JSON to `path`, atomically.

    Write-tmp-then-`os.replace`, the same guarantee `storage._write_index`
    gives a story: a save that dies halfway leaves the previous file
    intact rather than a truncated one the app can't read. The temporary
    file sits beside the target so the rename stays on one filesystem.

    Trailing newline so the files end the way every other text file here
    does, and `indent=2` so a person can read a diff of one.
    """
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)
