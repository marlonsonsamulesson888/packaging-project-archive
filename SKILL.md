---
name: packaging-project-archive
description: Organize a requested packaging-design project archive, verify copied file bytes, and disclose missing assets and restore limitations. Use for whole-project archiving, not a single artwork revision or print approval.
---

# Design project archive and integrity review

Build a recoverable, scoped project copy and an honest completeness report. A matching file copy is not proof that linked artwork, fonts, conversations, or every historical version was included.

## Establish scope

Identify the requested projects, source locations, intended destination, and whether the user wants an inventory or an actual copy. Do not infer authority to move, delete, overwrite, upload, or share material from permission to inspect. Preserve originals. Prefer a new dated destination over merging into an existing archive. Stop for an ambiguous destination or unreadable source rather than quietly omitting it.

Classify originals, editable masters, previews, dielines, linked images, requested history, and delivery files. Record exclusions and unavailable items. Do not collect account settings, credentials, unrelated correspondence, or licensed fonts merely to make the archive look complete. Record dependencies without redistributing them unless allowed.

## Copy and verify

After authorized copying, compare a stable source snapshot with the destination. For local regular files, run:

```sh
python scripts/verify_archive.py SOURCE COPY > verification.json
```

This helper is read-only, compares relative paths and SHA-256 bytes, rejects same/nested roots and symlinks, and emits an error when files change during hashing. Write its report outside both roots. It does not perform copying, parse document links, open design applications, or verify timestamps/ACLs/extended attributes. It does not freeze either filesystem; a concurrent edit after hashing can invalidate the result. Pause edits or use a snapshot where available.

A zero exit means only the two scanned regular-file sets matched at check time. Unreadable files, missing files, extra files, changed bytes and scan errors must remain visible. Retain source files even after a successful comparison; this skill never authorizes deleting originals.

## Test findability and restore

Use the report template in `assets/archive-report.md`. Open a proportionate sample of copied editable files in the intended application, check linked images/font availability, and record which ones were actually opened. A preview opening is not evidence that an AI/PSD master restores. If the application is unavailable, say the restore test was not performed.

Check that a colleague could locate the current master, approved reference and deliverable without interpreting private machine paths. Keep archive indexes private by default: filenames and paths can reveal customer information.

## Deliver precisely

Report copied and verified counts, errors, exclusions, missing dependencies, restore samples, and destination. Do not call a same-computer second-drive copy offsite backup or disaster recovery. State whether another independent/offsite copy exists only when verified. Do not claim complete chat history or fully self-contained production files unless that scope was independently checked.

For public demonstrations, use self-authored synthetic files only. The example in `references/synthetic-case.md` illustrates a scope boundary, not a real client order or a production certification.
