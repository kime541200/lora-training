"""Clean tagger captions and prepend trigger words.
usage: python3 fix_captions.py <dataset_subdir> "<trigger1,trigger2>" ["<drop_tag1,drop_tag2>"]
Triggers go first (set keep_tokens = number of triggers in the toml). Drop tags are removed
wherever they appear (tags that fight the trigger, or describe background/meta noise)."""
import glob, sys

d = sys.argv[1]
trigger = [t.strip() for t in sys.argv[2].split(",") if t.strip()]
drop = {t.strip() for t in (sys.argv[3] if len(sys.argv) > 3 else "").split(",") if t.strip()}
drop |= set(trigger)
for f in glob.glob(f"{d}/*.txt"):
    tags = [t.strip() for t in open(f).read().split(",") if t.strip()]
    tags = [t for t in tags if t not in drop]
    open(f, "w").write(", ".join(trigger + tags))
print("done")
