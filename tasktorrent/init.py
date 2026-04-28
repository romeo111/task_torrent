"""`tasktorrent init` — scaffold a TaskTorrent integration into a consumer repo.

Drops these files into the target repo:
  .tasktorrent.yaml                       (consumer config; you customize banned_sources etc.)
  chunks/example-chunk-<timestamp>.md     (reference chunk-spec; lint-able starting point)
  contributions/.gitkeep
  TASKTORRENT_ONBOARDING.md               (next-steps pointer for the consumer maintainer)

Idempotent: refuses to overwrite existing files unless --force.

Usage:
  python -m tasktorrent.init <consumer-name> [--root /path/to/repo] [--force]

For a richer starter kit (validators, claim bots, issue templates), see the
reference implementation at https://github.com/romeo111/cancer-autoresearch
under `scripts/tasktorrent/` and `.github/`. A future iteration of this
command will copy them in directly; v0.4 ships the minimum viable scaffold.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

SCAFFOLD_DIR = Path(__file__).parent / "_scaffold"


def _now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d-%H%M")


def render_template(src: Path, replacements: dict[str, str]) -> str:
    text = src.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def _write_if_absent(path: Path, content: str, force: bool) -> str:
    """Returns 'created' | 'skipped' | 'overwritten'."""
    if path.exists() and not force:
        return "skipped"
    action = "overwritten" if path.exists() else "created"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return action


ONBOARDING_NOTE = """# TaskTorrent onboarding — next steps

`tasktorrent init` just dropped the minimum-viable scaffold:

- `.tasktorrent.yaml` — your consumer config. **Customize `banned_sources` and `active_cap` before opening any chunk.**
- `chunks/{example_filename}` — reference chunk-spec. Replace it with a real chunk before opening a GitHub issue.
- `contributions/.gitkeep` — empty dir for contributor sidecars.

## What's NOT yet in your repo

The richer starter kit (validators, claim bots, issue templates, reverify
script templates) is not copied in by v0.4 of `tasktorrent init`. To wire
those up:

1. Copy the reference implementation from
   https://github.com/romeo111/cancer-autoresearch under
   `scripts/tasktorrent/` and `.github/`.
2. Adapt to your repo's banned-sources, KB layout, and Pydantic schemas.
3. Add `tasktorrent` to your dev dependencies and run the linter on every PR
   that touches `chunks/*.md`:

   ```yaml
   # .github/workflows/tasktorrent-lint.yml
   - run: pip install tasktorrent && python -m tasktorrent.lint_chunk_spec --all chunks/
   ```

## Validate your scaffold

```bash
python -m tasktorrent.lint_chunk_spec chunks/{example_filename}
```

## Open your first chunk

1. Replace the example chunk with a real one.
2. Re-lint until it passes.
3. Open a GitHub issue using the `chunk-task` template (copy from `cancer-autoresearch/.github/ISSUE_TEMPLATE/`).
4. Either claim it yourself or wait for a contributor.
"""


def init(consumer_name: str, root: Path, force: bool = False) -> dict[str, str]:
    """Scaffold a TaskTorrent integration. Returns {relative_path: status}."""
    if not root.is_dir():
        raise FileNotFoundError(f"target root does not exist: {root}")

    if not consumer_name or " " in consumer_name or consumer_name.lower() != consumer_name:
        raise ValueError(
            f"consumer_name must be lowercase with no spaces; got `{consumer_name}`"
        )

    stamp = _now_stamp()
    example_filename = f"example-chunk-{stamp}.md"

    results: dict[str, str] = {}

    # 1. .tasktorrent.yaml
    cfg_template = SCAFFOLD_DIR / ".tasktorrent.yaml.template"
    cfg_content = render_template(cfg_template, {"CONSUMER_NAME": consumer_name})
    cfg_path = root / ".tasktorrent.yaml"
    results[".tasktorrent.yaml"] = _write_if_absent(cfg_path, cfg_content, force)

    # 2. chunks/example-chunk-<stamp>.md
    chunk_template = SCAFFOLD_DIR / "chunk_example.md.template"
    chunk_content = render_template(chunk_template, {"CONSUMER_NAME": consumer_name})
    # Rewrite the example chunk-id inline to reflect the actual stamp
    chunk_content = chunk_content.replace(
        "example-chunk-2026-04-28-1700", f"example-chunk-{stamp}"
    )
    chunk_path = root / "chunks" / example_filename
    results[f"chunks/{example_filename}"] = _write_if_absent(chunk_path, chunk_content, force)

    # 3. contributions/.gitkeep
    contrib_path = root / "contributions" / ".gitkeep"
    results["contributions/.gitkeep"] = _write_if_absent(contrib_path, "", force)

    # 4. Onboarding note
    onboarding_path = root / "TASKTORRENT_ONBOARDING.md"
    onboarding_content = ONBOARDING_NOTE.format(example_filename=example_filename)
    results["TASKTORRENT_ONBOARDING.md"] = _write_if_absent(
        onboarding_path, onboarding_content, force
    )

    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tasktorrent.init",
        description="Scaffold a TaskTorrent integration into a consumer repo.",
    )
    parser.add_argument("consumer_name", help="lowercase identifier, no spaces (e.g. openonco)")
    parser.add_argument(
        "--root",
        default=".",
        help="path to the consumer repo root (default: cwd)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing files (default: skip)",
    )
    args = parser.parse_args(argv)

    try:
        results = init(args.consumer_name, Path(args.root).resolve(), force=args.force)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    for rel_path, status in results.items():
        print(f"  {status:12s} {rel_path}")

    print()
    print(f"Scaffold complete. Next: read TASKTORRENT_ONBOARDING.md in {args.root}.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
