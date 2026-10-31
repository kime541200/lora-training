# Lessons (from the sproutturtle / Illustrious run)

## Environment

- The container has no user entry for the host uid; torch fails with `getpwuid` unless `USER`/`LOGNAME` are set and `TORCHINDUCTOR_CACHE_DIR` points inside `/work`. `templates/run.sh` already does this; keep it.
- `max_train_epochs` in the toml overrides `--max_train_steps`; a short run means editing the epoch count.
- Training and ComfyUI share one GPU: stop one before the other.

## Data

- Transparent PNGs become a flat white background; the tagger then emits `transparent background`, `simple background`, `1boy`, `solo`, `no humans`, `outline` and species names that duplicate the trigger. Drop those tags so the background and "no humans" are put back deliberately (`fix_captions.py` third argument), and name the subject in the trigger (`sproutturtle, turtle`).
- Pass the tags that describe changeable things (pose, expression, held items) through. Tags describing the character's fixed look are the ones to remove when you want it baked into the trigger.

## Generation

- A single subject generates most reliably, matching a single-subject dataset. A collage of many small subjects appeared once in six seeds (5/6 normal) with no collage in the training set. Fixes that worked: change the seed, or add `multiple views, character sheet, sprite sheet, collage, multiple characters` to the negative prompt. Root cause unconfirmed.
- Seed sweep (1–6) on every test prompt: one seed is an anecdote.

## Next knob when the result is poor

| Symptom | Try |
| --- | --- |
| Weak likeness | more epochs or repeats; use a later checkpoint |
| Ignores the prompt, burnt colours, memorised poses | earlier checkpoint; lower lr or dim; add image variety |
| Trigger works but style leaks everywhere | more varied backgrounds in the data; check captions did not drop the background tags |
