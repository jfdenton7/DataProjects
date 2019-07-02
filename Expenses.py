from PyPDF2 import PdfFileReader
import re
import matplotlib.pyplot as plt
import numpy as np
import operator

"""
Reads bank statements from USAA, printing out avarage cost
per day and graph with corresponding graph
"""


def parse_text(text_full: str):
    return text_full.split('\n')


with open("CpEddDocumentView.pdf", "rb") as fp:
    totalCosts = []
    pdf = PdfFileReader(fp)
    dateLine = re.compile(r'(.*)\d\d/\d\d(.*)')
    cost = re.compile(r'(\d*)\.(\d*)')
    words = re.compile(r'[a-zA-Z]]')
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        text = page.extractText()
        text_list = parse_text(text)
        run = False
        for line in text_list:
            if "OTHER DEBITS" in line:
                run = True
            mo = dateLine.search(line)

            if mo and run:
                momo = cost.search(line)
                if momo:
                    day = (str(mo.group()).split(' '))
                    day = list(filter(lambda x: len(x) > 0, day))
                    totalCosts.append(day)

    for _ in range(11):
        totalCosts.pop()

costsCleaned = {}

for cost in totalCosts:
    cost[1] = cost[1].replace(',', '')

    if cost[0] not in costsCleaned:
        costsCleaned[cost[0]] = float(cost[1])
    else:
        costsCleaned[cost[0]] += float(cost[1])

sorted_costs = sorted(costsCleaned.items(), key=operator.itemgetter(0))
dates = []
costs = []
costs_modif = []
for cost in sorted_costs:
    dates.append(cost[0])
    costs.append(cost[1])
    if int(cost[1]) < 1000:
        costs_modif.append(cost[1])

print("AVG COST PER DAY: $" + str(sum(costs)/len(costs)))

plt.bar(height=costs, x=dates, linewidth=10.0)
plt.xticks(np.arange(len(dates)), dates, rotation=40)
plt.yticks([x for x in range(0, 1500, 50)])
plt.show()

