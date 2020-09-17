#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests
import sys
import os

COURSE_MATERIALS = [
    "Logic",
    "Prog Dyn",
    "Neural Net",
    "BD",
    "Adv Prog",
    "Archi HPerf",
    "AI Game",
    "Challenge",
    "CriticalSyst",
    "Calc",
    "TATIA",
    "Comp Net",
    "Reso Pb",
    "TER",
    "Parallelism",
    "IoT"
]

URL = "http://i3s.unice.fr/master-info/edt/m1/"

def example ():
    print("Usage:\n\tpython3 {0}".format(sys.argv[0]))
    sys.exit(2)

def get_sheet (u):
    print("[*] Requesting {}".format(u))
    r = requests.get(u)
    sheet_url = re.findall(r"https:\/\/docs\.google\.com\/spreadsheets.* ", r.text)[0].split(" ")[0].replace("true","false")
    print("[*] Sheet url with array in HTML found: {}".format(sheet_url))
    r = requests.get(sheet_url)
    sheet = r.text
    p = re.compile("\/static")
    sheet = p.sub("https://docs.google.com/static", sheet)
    return sheet

# Remove all non-used lessons and the bg colour in their html bloc
def parse (sheet, lessons):
    choosed = [l.split("\n")[0].split("\r\n")[0] for l in lessons.readlines()]
    reverted_lessons = [lesson for lesson in COURSE_MATERIALS if lesson not in choosed]

    for lesson in reverted_lessons:
        l = lesson.split("\n")[0].split("\r\n")[0]
        regex = "{}{}{}".format(" (\w+=\"(\w|\d| )+\")*>(<div class=\"(\w|-)+\" style=\"width: \d+px; left: -\d+px;\">)?",l,"(</div>)?")
        p = re.compile(regex)
        sheet = p.sub(">", sheet)
    
    return sheet

def main ():
    if len(sys.argv) > 1:
        example()

    sheet = get_sheet(URL)
    try:
        lessons = open("config.txt", "r")
        edt = open("EDT.html", "w+")
        new_sheet = parse(sheet, lessons)
        edt.write(new_sheet)

        lessons.close()
        edt.close()
        print("[*] The parsed file is saved as EDT.html in your current working directory")
    except IOError:
        print("[!] config.txt file not found exception")
        sys.exit(2)

if __name__ == '__main__':
    main()
