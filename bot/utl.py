# This file is in the Public Domain.


def consume(events):
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


def spl(txt):
    return [x for x in txt.split(",") if x]
