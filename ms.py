# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:01:57 2023

@author: rikuk
"""

import mechanicalsoup
from bs4 import BeautifulSoup


def getAssessments(page):
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(class_="unit-guide-header-container")
    subject = title.h1  # finds the title
    time = title.h3  # finds the date
    print(subject.text)
    print(time.text)
    print("")

    assessments = soup.find_all(class_="assessment-task-info")
    desc = soup.find_all(class_="info-description")
    for ass, des in zip(assessments, desc):
        print(ass.h3.text)  # prints assessments, weighting and descriptions
        print(ass.p.text)
        print(des.text)


def main():
    val = input("Enter unit code: ")
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )
    browser.set_user_agent('Mozilla/5.0')

    browser.open("https://unitguides.mq.edu.au/units")  # opens unit guide
    # NEED TO CHANGE PER YEAR
    browser.select_form('form[action="/units/search/2023"]')
    browser['query'] = val
    browser.submit_selected()
    try:  # if current unit guide is found
        found = browser.follow_link(class_="unit-guide-list-item")
        getAssessments(found)
    except:
        try:  # If no current unit guide is found
            browser.follow_link("a", text="search archived unit guides")
            browser.select_form('form[action="/units/archive_search"]')
            browser.submit_selected()
            foundold = browser.follow_link(class_="unit-guide-list-item")
            print("This is an old version of " + val +
                  ". It may have changed this year.")
            getAssessments(foundold)
        except:
            print("none found")


if __name__ == "__main__":
    main()
