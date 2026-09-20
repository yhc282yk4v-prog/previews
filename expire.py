"""Delete preview folders whose expiry time has passed. Runs on GitHub Actions, not on anyone's laptop."""
import datetime, json, pathlib, shutil

root = pathlib.Path(__file__).parent
mf = root / "manifest.json"
data = json.loads(mf.read_text())
now = datetime.datetime.now(datetime.timezone.utc)
changed = False
for slug, info in list(data.get("previews", {}).items()):
    exp = datetime.datetime.fromisoformat(info["expires"].replace("Z", "+00:00"))
    if exp <= now:
        d = root / slug
        if d.is_dir():
            shutil.rmtree(d)
        data["previews"].pop(slug)
        data.setdefault("expired", {})[slug] = info["expires"]
        print("taken down:", slug)
        changed = True
if changed:
    mf.write_text(json.dumps(data, indent=2) + "\n")
else:
    print("nothing expired")
