#!/usr/bin/python3
"""Markdown python file"""
import hashlib
import os
import re
import sys


def remove_c_inline(ln=""):
    """remove letter c in the line"""
    text = ""
    new = ""
    if ln.find("((") != -1 and ln.find("))") != -1:
        reg_exp = '{}({}(|{}){})'.format('\\', '\\', '\\', '\\')
        spline = re.split(reg_exp, ln)
        for i in range(len(spline)):
            if i % 2 != 0:
                for j, char in enumerate(spline[i]):
                    if char != 'C' and char != 'c':
                        new += char
                text += new
            else:
                text += spline[i]
        return text
    else:
        return ln


def parse_inline_to_md5(ln=""):
    """replace [[text]] to MD5"""
    text = ""
    if ln.find("[[") != -1 and ln.find("]]") != -1:
        reg_exp = '{}[{}[|{}]{}]'.format('\\', '\\', '\\', '\\')
        spline = re.split(reg_exp, ln)
        for i in range(len(spline)):
            if i % 2 != 0:
                hash_object = hashlib.md5(spline[i].encode())
                md5_hash = hash_object.hexdigest()
                text += md5_hash
            else:
                text += spline[i]
        return text
    else:
        return ln


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
    # Validate arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing {}\n".format(sys.argv[1]))
        exit(1)

    # Input file
    fr = open(sys.argv[1], 'r')
    inFile = fr.read().split('\n')

    # Output file
    fw = open(sys.argv[2], 'w')

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
                        fw.write("{}{}{}".format(hOpTags[head],
                                                 hText,
                                                 hClTags[head]))
                        break

            # Validate unordered lists
            if line.find('- ') == 0:
                if isUlOpened is False:
                    fw.write('<ul>\n')
                    isUlOpened = True
                lText = line.split('- ')
                lText[1] = add_inline_tags(lText[1], "**", "<b>", "</b>")
                lText[1] = add_inline_tags(lText[1], "__", "<em>", "</em>")
                lText[1] = parse_inline_to_md5(lText[1])
                lText[1] = remove_c_inline(lText[1])
                fw.write('<li>{}</li>'.format(lText[1]))

            # Validate ordered lists
            if line.find('* ') == 0:
                if isOlOpened is False:
                    fw.write('<ol>\n')
                    isOlOpened = True
                lText = line.split('* ')
                lText[1] = add_inline_tags(lText[1], "**", "<b>", "</b>")
                lText[1] = add_inline_tags(lText[1], "__", "<em>", "</em>")
                lText[1] = parse_inline_to_md5(lText[1])
                lText[1] = remove_c_inline(lText[1])
                fw.write('<li>{}</li>'.format(lText[1]))

            # Validate empty line
            if line != '':
                fw.write('\n')
        else:
            # close previous lists
            if isUlOpened is True:
                isUlOpened = False
                fw.write('</ul>\n')
            if isOlOpened is True:
                isOlOpened = False
                fw.write('</ol>\n')

            if isPOpened is False and line != '':
                fw.write('<p>\n')
                isPOpened = True

            if isPOpened is True and line != '':
                line = add_inline_tags(line, "**", "<b>", "</b>")
                line = add_inline_tags(line, "__", "<em>", "</em>")
                line = parse_inline_to_md5(line)
                line = remove_c_inline(line)
                if isPreText is False:
                    fw.write('{}'.format(line))
                    isPreText = True
                else:
                    fw.write('\n<br/>\n{}'.format(line))
            elif isPOpened is True:
                isPOpened = False
                isPreText = False
                fw.write('\n</p>\n')

    # close HTML file
    fw.close()
