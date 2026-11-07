"""Extract the player-visible strings of Avadon Files/AvScenData.dat.

usage:
    python -I scen_extract.py ORIGINAL_AVSCENDATA OUT_DIR

File layout (from Avadon.exe 0x4283f0 / 0x4284a0):
    0x000000  header, 0x1168 bytes (loaded to 0x738478): zone count, then zone entries of
              0x2c bytes from +4: name (field 0x28), 4 bytes of data
    0x001168  24 zones, 0x3d42c bytes each (loaded to 0x97f8b0)
String fields used here (zone-relative offset, count, stride, field size):
    map labels  +0x16054 10 x 0x28   (positions at +0x16004; code 0x456c10)
    area names  +0x2c24c 10 x 0x28
(script names after +0x2c3f0 are not shown in game.)

Writes OUT_DIR/units.json: [{"id", "kind", "en", "max_bytes", "fields": [[file offset, size]]}]
with identical (kind, English) entries merged.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

HEAD = (0x4, 0x2c, 100)
ZONE = (0x1168, 0x3d42c, 24)
# kind, record set, first offset, count, stride, field size, max bytes for a translation
FIELDS = [
    ('zone name', HEAD, 0x0, 1, 0, 0x28, 39),
    ('zone label', ZONE, 0x16054, 10, 0x28, 0x28, 39),
    ('zone area', ZONE, 0x2c24c, 10, 0x28, 0x28, 39),
]
TEXT = re.compile(rb'[\x20-\x7e]*[A-Za-z]{2}[\x20-\x7e]*')


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    src, out = argv
    d = open(src, 'rb').read()
    units = {}
    for kind, (base, size, n), first, count, stride, fsize, maxb in FIELDS:
        for r in range(n):
            for k in range(count):
                off = base + r * size + first + k * stride
                field = d[off:off + fsize]
                z = field.find(b'\0')
                if z <= 0:
                    continue
                s = field[:z]
                if not TEXT.fullmatch(s) or s == b'Zone Name':
                    continue
                en = s.decode('ascii')
                key = (kind.split()[1], en)
                u = units.get(key)
                if u is None:
                    u = units[key] = {'id': f'{kind.split()[1]}{len(units):04d}', 'kind': kind, 'en': en,
                                      'max_bytes': maxb, 'fields': []}
                u['max_bytes'] = min(u['max_bytes'], maxb)
                u['fields'].append([off, fsize])
    os.makedirs(out, exist_ok=True)
    lst = list(units.values())
    with open(os.path.join(out, 'units.json'), 'w', encoding='utf-8') as f:
        json.dump(lst, f, ensure_ascii=False, indent=0)
    by = {}
    for u in lst:
        by[u['kind']] = by.get(u['kind'], 0) + 1
    print(len(lst), 'unique strings', sum(len(u['fields']) for u in lst), 'fields', by,
          sum(len(u['en']) for u in lst), 'chars')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
