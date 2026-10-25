import re, sys

svg = open(sys.argv[1] if len(sys.argv) > 1 else "bt_unificado.svg").read()

paths_raw = re.findall(r'<path d="([^"]+)"', svg)
bad_angle = 0
for p in paths_raw:
    nums = re.findall(r'[-\d.]+', p)
    pts = [(float(nums[i]), float(nums[i+1])) for i in range(0, len(nums), 2)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if abs(x1 - x2) > 0.5 and abs(y1 - y2) > 0.5:
            print('DIAGONAL:', (x1, y1), (x2, y2))
            bad_angle += 1

shapes = []
for m in re.finditer(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)" rx="5"', svg):
    x, y, w, h = map(float, m.groups())
    shapes.append(('caja', x, y, x + w, y + h))
for m in re.finditer(r'<polygon points="([^"]+)"', svg):
    coords = [tuple(map(float, pt.split(','))) for pt in m.group(1).split()]
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    shapes.append(('rombo', min(xs), min(ys), max(xs), max(ys)))


def segs(p):
    nums = re.findall(r'[-\d.]+', p)
    pts = [(float(nums[i]), float(nums[i + 1])) for i in range(0, len(nums), 2)]
    return list(zip(pts, pts[1:]))


def crosses(p1, p2, shape):
    x1, y1 = p1
    x2, y2 = p2
    _, bx0, by0, bx1, by1 = shape
    if abs(x1 - x2) < 0.5:
        if not (bx0 < x1 < bx1):
            return False
        lo, hi = sorted([y1, y2])
        return hi > by0 + 2 and lo < by1 - 2
    else:
        if not (by0 < y1 < by1):
            return False
        lo, hi = sorted([x1, x2])
        return hi > bx0 + 2 and lo < bx1 - 2


bad_cross = 0
for p in paths_raw:
    for (p1, p2) in segs(p):
        for s in shapes:
            if crosses(p1, p2, s):
                print('CRUZA', s[0].upper() + ':', p1, p2, s[1:])
                bad_cross += 1

print(f'diagonales={bad_angle} cruces={bad_cross} (trazos={len(paths_raw)}, formas={len(shapes)})')
sys.exit(1 if (bad_angle or bad_cross) else 0)
