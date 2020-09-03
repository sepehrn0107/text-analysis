
import csv

def prepareData(filename, author, csv_file):
    with open(filename, encoding='utf-8') as f:
        data = [x.strip() for x in f.readlines() if len(x) > 2]

    with open(csv_file, 'r') as c:
        try:
            opened_file = c.readlines()
            i = int(opened_file[-2].split(',')[0]) + 1
        except:
            i = 0
    with open(csv_file, 'a') as w:
        writer = csv.writer(w)
        for item in data:
            writer.writerow([i, str(item), author])
            i += 1



prepareData('samples/Train/CHARLESDICKENS.txt', 'CD', 'samples/Train/samplecsv.csv')


prepareData('samples/Train/OHENRY.txt', 'OH', 'samples/Train/samplecsv.csv')


prepareData('samples/Train/OSCARWILDE.txt', 'OW', 'samples/Train/samplecsv.csv')




