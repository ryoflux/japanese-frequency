import json
from sys import argv


def detect_script(char):
    if "\u4e00" <= char <= "\u9fbf":
        return "kanji"
    elif "\u3040" <= char <= "\u309F":
        return "hiragana"
    elif "\u3000" <= char <= "\u303F" or "\uFF00" <= char <= "\uFFEF":
        return "punctuation"
    elif "\u30A0" <= char <= "\u30FF":
        return "katakana"
    elif "\u0000" <= char <= "\u007F":
        return "latin"
    else:
        raise ValueError(f"Unknown character {char}")


with open(argv[1], "r") as f:
    dictionary = {}
    for char in f.read():
        if char in dictionary:
            dictionary[char]["count"] += 1
        else:
            try:
                dictionary[char] = {"count": 1, "script": detect_script(char)}
            except:
                pass

    del dictionary["\n"]
    del dictionary["　"]
    del dictionary[" "]
    dictionary = dict(sorted(dictionary.items(), key=lambda i: -i[1]["count"]))

    counts = {"kanji": 0, "hiragana": 0, "katakana": 0, "punctuation": 0, "latin": 0}
    uniqueCounts = {
        "kanji": 0,
        "hiragana": 0,
        "katakana": 0,
        "punctuation": 0,
        "latin": 0,
    }

    for k, v in dictionary.items():
        counts[v["script"]] += v["count"]
        uniqueCounts[v["script"]] += 1

    countsTotal = sum([v["count"] for k, v in dictionary.items()])
    uniqueTotal = sum([v for k, v in uniqueCounts.items()])

    results = {
        "total": countsTotal,
        "uniqueTotal": uniqueTotal,
        "count": {
            k: {"count": v, "percent": f"{round(v / countsTotal, 2) * 100}%"}
            for k, v in counts.items()
        },
        "uniqueCount": {
            k: {"count": v, "percent": f"{round(v / uniqueTotal, 2) * 100}%"}
            for k, v in uniqueCounts.items()
        },
        "characters": dictionary,
    }

    with open("results.json", "w") as jf:
        json.dump(results, jf, indent=4, ensure_ascii=False)
