"""Rewrite the countdown block in README.md (between the marker comments)."""
import json, re, datetime as dt, urllib.parse, pathlib

root = pathlib.Path(__file__).resolve().parents[2]
cfg = json.loads((root / "countdown.json").read_text())
end = dt.datetime.fromisoformat(cfg["end_utc"].replace("Z", "+00:00"))
now = dt.datetime.now(dt.timezone.utc)
ist = dt.timezone(dt.timedelta(hours=3))
end_txt = f"{end.astimezone(ist):%d %b %Y, %H:%M} Istanbul (UTC+3) / {end:%d %b %Y, %H:%M} UTC"

def badge(label, msg, color):
    q = lambda s: urllib.parse.quote(s.replace("-", "--").replace("_", "__"), safe="")
    return f"https://img.shields.io/badge/{q(label)}-{q(msg)}-{color}?style=for-the-badge"

left = (end - now).total_seconds()
if left > 0:
    h, m = int(left // 3600), int(left % 3600 // 60)
    msg = f"{h}h {m:02d}m left"
    block = (f"![Community snapshot: {msg}]({badge('community snapshot', msg, 'e10600')})\n\n"
             f"**Community snapshot closes in {h}h {m:02d}m**, at {end_txt}.")
else:
    block = (f"![Community snapshot closed]({badge('community snapshot', 'closed', '555555')})\n\n"
             f"**Community snapshot closed** ({end_txt}).")

readme = root / "README.md"
text = readme.read_text()
new = re.sub(r"(<!-- countdown:start -->\n).*?(\n<!-- countdown:end -->)",
             lambda mm: mm.group(1) + block + mm.group(2), text, flags=re.S)
if new != text:
    readme.write_text(new)
    print("updated:", block.splitlines()[-1])
else:
    print("no change")
