#!/usr/bin/python3
"""Markdown python file"""
import hashlib
import os
import re
import sys

def add_inline_tags(ln="", st="", o_tag="", c_tag=""):
    """Insert inline tags on README line"""
    text = ""
    tag_opened = False
    if ln.find(st) != -1 and ln.find(st, 1) != -1:
        spline = ln.split(st)
        for i in range(len(spline)):
            if i % 2 != 0 and tag_opened is False:
                text += o_tag
                tag_opened = True
            elif i % 2 == 0 and tag_opened is True:
                text += c_tag
                tag_opened = False
            text += spline[i]
        if text.find(o_tag + c_tag) != -1:
            text = text.replace(o_tag + c_tag, st + st)
        return text
    else:
        return ln


headers = ["###### ", "##### ", "#### ", "### ", "## ", "# "]
hOpTags = {headers[0]: "<h6>", headers[1]: "<h5>", headers[2]: "<h4>",
           headers[3]: "<h3>", headers[4]: "<h2>", headers[5]: "<h1>"}
hClTags = {headers[0]: "</h6>", headers[1]: "</h5>", headers[2]: "</h4>",
           headers[3]: "</h3>", headers[4]: "</h2>", headers[5]: "</h1>"}
isUlOpened = False
isOlOpened = False
isPOpened = False
isPreText = False

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r') as inFile, open(output_file, 'w') as fw:
        for line in inFile:
            # Validate first 2 characters
            if line.find('# ') == 0 or line.find('##') == 0 or \
                    line.find('- ') == 0 or line.find('* ') == 0:

                # close previous paragraph
                if isPOpened is True:
                    isPOpened = False
                    isPreText = False
                    fw.write('\n</p>\n')

                # Validate heading levels
                if line.find('#') == 0:
                    for head in headers:
                        if line.find(head) == 0:
                            hText = line.split(head)[1]
                            hText = add_inline_tags(hText, "**", "<b>", "</b>")
                            hText = add_inline_tags(hText, "__", "<em>", "</em>")
                            fw.write("{}{}{}".format(hOpTags[head], hText.strip(), hClTags[head]))
                            fw.write("\n")
                            break

    sys.exit(0)
