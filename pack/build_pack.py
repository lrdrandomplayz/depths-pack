"""Builds DepthsGuard-pack.zip from the vanilla client jar.

Every file in the pack is an untouched vanilla file. Because the server pack
always loads above the player's own packs, these copies win over any xray or
invis-particle pack that edits the same paths.
"""
import hashlib, json, os, sys, zipfile
from pathlib import Path

HERE = Path(__file__).parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else "1.21.11"
JAR = Path(os.environ["APPDATA"]) / ".minecraft" / "versions" / VERSION / f"{VERSION}.jar"
OUT = HERE / "DepthsGuard-pack.zip"
MC = "assets/minecraft/"


def lines(name):
    return [l.strip() for l in (HERE / name).read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def ref(name, folder):
    # "minecraft:block/stone" or "block/stone" -> assets/minecraft/<folder>/block/stone
    name = name.split(":", 1)[-1]
    return f"{MC}{folder}/{name}"


def main():
    jar = zipfile.ZipFile(JAR)
    names = set(jar.namelist())
    wanted = set()

    def add(path):
        if path in names:
            wanted.add(path)
            if path + ".mcmeta" in names:  # animated textures
                wanted.add(path + ".mcmeta")
            return True
        return False

    seen_models = set()

    def add_model(model):
        path = ref(model, "models") + ".json"
        if path in seen_models:
            return
        seen_models.add(path)
        if not add(path):
            return  # builtin/generated etc.
        data = json.loads(jar.read(path))
        if "parent" in data:
            add_model(data["parent"])
        for tex in data.get("textures", {}).values():
            if not tex.startswith("#"):
                add(ref(tex, "textures") + ".png")

    def walk_models(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "model" and isinstance(v, str):
                    add_model(v)
                else:
                    walk_models(v)
        elif isinstance(node, list):
            for v in node:
                walk_models(v)

    missing = []
    for block in lines("blocks.txt"):
        bs = f"{MC}blockstates/{block}.json"
        if not add(bs):
            missing.append(block)
            continue
        walk_models(json.loads(jar.read(bs)))

    for extra in lines("extra.txt"):
        full = MC + extra
        if extra.endswith("/"):
            hits = [n for n in names if n.startswith(full) and not n.endswith("/")]
            if not hits:
                missing.append(extra)
            wanted.update(hits)
        elif not add(full):
            missing.append(extra)

    if missing:
        sys.exit(f"Not in {VERSION} jar: {', '.join(missing)}")

    fmt = json.loads(jar.read("version.json"))["pack_version"]["resource_major"]
    mcmeta = {
        "pack": {
            "description": "§5The Depths SMP §7– required pack",
            "pack_format": fmt,
            # Newer clients read min/max_format, older ones supported_formats.
            "min_format": 34,
            "max_format": 99,
            "supported_formats": [34, 99],
        }
    }

    OUT.unlink(missing_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("pack.mcmeta", json.dumps(mcmeta, indent=2, ensure_ascii=False))
        if (HERE / "pack.png").exists():
            z.write(HERE / "pack.png", "pack.png")
        for n in sorted(wanted):
            info = zipfile.ZipInfo(n, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, jar.read(n))

    sha1 = hashlib.sha1(OUT.read_bytes()).hexdigest()
    (HERE / "DepthsGuard-pack.sha1").write_text(sha1 + "\n")
    print(f"{len(wanted)} vanilla files, pack_format {fmt}, {OUT.stat().st_size // 1024} KB")
    print(f"sha1 {sha1}")


if __name__ == "__main__":
    main()
