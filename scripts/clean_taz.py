#!/usr/bin/env python3

import sys
import re


if len(sys.argv) != 3:
    print("usage: clean.py input.html output.html")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

needle = '<section class="outerwrapper ' 
pos = 0
out = []

while True:
    start = text.find(needle, pos)
    if start == -1:
        break

    i = start
    depth = 0

    while i < len(text):
        if text.startswith("<section", i):
            depth += 1
            i += 4
        elif text.startswith("</section>", i):
            depth -= 1
            i += 6

            if depth == 0:
                block = text[start:i]
                out.append(block)
                pos = i
                break
        else:
            i += 1
    else:
        # EOF erreicht ohne schließendes </section>
        break

def remove_html_blocks(tag_start, tag_end, text):
    pos = 0
    out = []

    while True:
        start = text.find(tag_start, pos)
        if start == -1:
            out.append(text[pos:])
            break

        out.append(text[pos:start])

        end = text.find(tag_end, start)
        if end == -1:
            # kaputtes HTML → alles ab <svg> weg
            break

        pos = end + len(tag_end)

    return "".join(out)

result = "\n".join(out)
#result = remove_html_blocks("<svg", "</svg>", result)
#result = remove_html_blocks("<button", "</button>", result)
#result = remove_html_blocks("<script", "</script>", result)
result = re.sub(r'>\s+<', '><', result)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(result)

