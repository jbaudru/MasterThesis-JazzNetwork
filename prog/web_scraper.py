import nltk
import requests
import pandas as pd
import csv
import re
import unidecode

from bs4 import BeautifulSoup

def main():
    print('==========================================')
    filter = txt_to_lst("../data/filter_words.txt")
    tmp_lst = txt_to_lst("../data/filter_producers.txt")
    filter.extend(tmp_lst)
    tmp_lst = txt_to_lst("../data/filter_writers.txt")
    filter.extend(tmp_lst)
    tmp_lst = txt_to_lst("../data/filter_labels.txt")
    filter.extend(tmp_lst)
    #words_eng = set(nltk.corpus.words.words('en'))
    #filter.extend(words_eng)

    # web_scrapping_site_1()

    """
    print("Building dataset #2")
    web_scrapping_site_2(filter, "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Album_de_jazz", "data2.csv", "mw-category-group", "class" )
    print("Building dataset #3")
    web_scrapping_site_3(filter, "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Album_de_jazz_am%C3%A9ricain", "data3.csv", "mw-category", "class")
    print("Building dataset #4")
    web_scrapping_site_3(filter, "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Album_de_jazz_fran%C3%A7ais", "data4.csv", "mw-category", "class")
    print("Building dataset #5")
    web_scrapping_site_3(filter, "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Album_de_jazz_fusion", "data5.csv", "mw-category", "class")
    print("Building dataset #6")
    web_scrapping_site_4(filter, "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Album_de_bossa_nova", "data6.csv", "mw-category", "class")
    print('==========================================')
    """


    num = 7
    for i in range(600, 10000, 300): #37000 upper bound
        filename = "data" + str(num) + "c.csv"
        print("\nBuilding ", filename)
        web_scrapping_jazz_montreux("https://database.montreuxjazz.com/", i, i + 300, filename, filter)
        num += 1


# Get data from Wiki with Pandas, Tables from website are converted in Dataframes
def web_scrapping_site_1():
    url1 = "https://fr.wikipedia.org/wiki/Liste_des_albums_de_jazz_les_plus_vendus"
    df_list = pd.read_html(url1)
    path = "../data/"
    name = path + "data1.csv"
    file = open(name, 'w')
    spamWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(df_list)):
        for index, row in df_list[i].iterrows():
            tmp_lst = [str(row[1][2::]), str(row[2])]
            # Cleaning dataset
            for k in range(0, len(tmp_lst)):
                tmp_lst[k] = tmp_lst[k].replace('\u2194', '')
                tmp_lst[k] = tmp_lst[k].replace('Others', '')
                tmp_lst[k] = tmp_lst[k].replace('\n', '')
                tmp_lst[k] = tmp_lst[k].replace('others', '')
                tmp_lst[k] = tmp_lst[k].replace('Featuring', ',')
                tmp_lst[k] = tmp_lst[k].replace('featuring', ',')
                tmp_lst[k] = tmp_lst[k].replace('ft.', ',')
                tmp_lst[k] = tmp_lst[k].replace(' And', ',')
                tmp_lst[k] = tmp_lst[k].replace(' and', ',')
                tmp_lst[k] = tmp_lst[k].replace('&', ',')
                tmp_lst[k] = tmp_lst[k].replace('’', '')
                tmp_lst[k] = tmp_lst[k].replace('…', '')
                tmp_lst[k] = tmp_lst[k].replace('+', ',')
                tmp_lst[k] = tmp_lst[k].replace('/', ',')
                tmp_lst[k] = tmp_lst[k].replace('\xa0', '')
                tmp_lst[k] = unidecode.unidecode(tmp_lst[k])
            if(len(tmp_lst[0]) != 4): # Avoid void element
                if("Compilation" not in tmp_lst[1]): # Avoid compilation
                    if(i != 0 and index != 0): # Avoid misscrapping data
                        tmp_lst[0] = tmp_lst[0].upper()
                        tmp_lst[0] = re.sub('\[[^>]+\]', '', tmp_lst[0]) # Delete eveything between brackets
                        tmp_lst[0] = re.sub('\([^>]+\)', '', tmp_lst[0]) # Delete eveything between parenthesis in album name
                        tmp_lst[1] = re.sub('\([^>]+\)', '', tmp_lst[1]) # Delete eveything between parenthesis in musician name
                        tmp_lst[0] = tmp_lst[0].replace('"', '')
                        tmp_lst[1] = tmp_lst[1].replace('"', '')
                        if(tmp_lst[1] != ''):
                            tmp_lst.insert(1, "date")
                            tmp_lst.insert(2, "label")
                            print(tmp_lst)
                            spamWriter.writerow(tmp_lst)


# Get data from Wiki with BeautifulSoup and NLP
def web_scrapping_site_2(filter, url1, datasetname, flaghtml, typeflag):
    spamWriter, tmp = get_webpage(url1, datasetname, flaghtml, typeflag)
    tmp_lst = tmp[6::]
    get_indent_webpage(tmp_lst, spamWriter, filter)


# Get data from Wiki with BeautifulSoup and NLP
def web_scrapping_site_3(filter, url1, datasetname, flaghtml, typeflag):
    spamWriter, tmp = get_webpage(url1, datasetname, flaghtml, typeflag)
    tmp_lst = tmp[1]
    get_indent_webpage(tmp_lst, spamWriter, filter)


# Get data from Wiki with BeautifulSoup and NLP
def web_scrapping_site_4(filter, url1, datasetname, flaghtml, typeflag):
    spamWriter, tmp = get_webpage(url1, datasetname, flaghtml, typeflag)
    tmp_lst = tmp[0]
    get_indent_webpage(tmp_lst, spamWriter, filter)


def web_scrapping_jazz_montreux(url, x, y, datasetname, filter):
    path = "../data/"
    name = path + datasetname
    file = open(name, 'w')
    spamWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    data = {}

    for j in range(x, y): #650, 37300
        dataUrl = "concertdb_display.php?artistNid=" + str(j) + "&artistString=undefined&year=undefined&venueTid=undefined"

        _, tmpmu = get_webpage(url + dataUrl, datasetname, "concertsdb-list-detail-section", "class")
        _, tmptitle = get_webpage(url + dataUrl, datasetname, "concertsdb-list-title-detail", "class", True)
        tmpLst = str(tmpmu).split("\n")
        musician = []
        title = ""
        year = ""
        tmpMusic = ""

        csvlst = []

        if(len(tmptitle) > 0):
            brutpagetitle = str(tmptitle).split(">")[1].split(",")
            year = brutpagetitle[1].split(" ")[-1]
            titletmp = brutpagetitle[0].split(" ")
            for elem in titletmp:
                if(elem != "" and elem != "\n"):
                    title += elem + " "

            if(title not in data or data[title] != year): #avoid duplicate data
                if(len(tmpLst) > 1):
                    for elem in tmpLst[1].split(",")[0:-1]:
                        if(elem[-6:] == "</div>"):
                            elem = elem[:-6]

                        if(elem[0]== " "): #delete space at the beggging
                            ind = 0
                            while(elem[ind] == " "):
                                ind+=1
                            elem = elem[ind:]

                        if(elem[-1]== " "): #delete space at the end
                            ind = 1
                            while(elem[-ind] == " "):
                                ind+=1
                            elem = elem[:ind]

                        if(len(elem.split(" ")) > 1 and len(elem.split(" ")[0]) > 1): # avoid one lenght data (name) or (instrument) lonely, different form (name, instrument)
                            if(elem != "el-p)" and elem != "backing vocals)" and elem != "sampler)"):
                                musician.append(elem)

                if(len(musician) != 0):
                    csvlst.append(unidecode.unidecode(title))
                    csvlst.append(year)
                    print(title, year, j)
                    csvlst.append("label")
                    strmusi = ""
                    for i in range(0, len(musician)):
                        if(i != len(musician)-1):
                            strmusi += musician[i] + ","
                        else:
                            strmusi += musician[i]
                    csvlst.append(unidecode.unidecode(strmusi))
                    spamWriter.writerow(csvlst) #csvlst doit avoir le format : Title, Year, Label, Lst Musicians

            if(title not in data):
                data[title] = year

    file.close()

def get_webpage(url1, datasetname, flaghtml, typeflag, a=False):
    req = requests.Session()
    result = req.get(url1, timeout=10)
    soup = BeautifulSoup(result.content.decode('utf-8'), 'html.parser')
    if(a):
        tmp = soup.findAll('a', {typeflag: flaghtml})
    else:
        tmp = soup.findAll('div', {typeflag: flaghtml})
    path = "../data/"
    name = path + datasetname
    file = open(name, 'w')
    spamWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    return spamWriter, tmp


def get_indent_webpage(tmp_lst, spamWriter, filter):
        req = requests.Session()
        for elem in tmp_lst:  # For each catégorie
            for k in elem:
                for line in k:
                    tmp_lst = []
                    for link in line:
                        lk = str(link)
                        st = lk.find("href")
                        if(st != -1): # If there is a link to the ablum page
                            ed = lk.find("title")
                            final_lk = "https://fr.wikipedia.org" + lk[st+len("href")+2:ed-2]
                            res = req.get(final_lk, timeout=10)
                            sp = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
                            musicians = get_human_names(str(sp), filter)
                            year = get_collaboration_year(str(sp))
                        for title in link:
                            if(len(title) != 1):  # Avoid title of list in the Wiki page
                                title = unidecode.unidecode(title)
                                title = title.upper()
                                tmp_lst.append(title)  # Alb name
                                tmp_lst.insert(1, year)
                                tmp_lst.insert(2, "label")
                                musicians = unidecode.unidecode(musicians)
                                tmp_lst.insert(3, musicians)  # A faire recherche sur le lien (link)
                                spamWriter.writerow(tmp_lst)


def txt_to_lst(filename):
    lst = []
    file = open(filename, 'r')
    for line in file:
        line = line.replace('\n', '')
        lst.append(line)
    return lst


def get_collaboration_year(text):
    year = "year"
    ind_tmp_year = text.find("sorti en ")
    tmp_year = text[ind_tmp_year+len("sorti en "):ind_tmp_year+len("sorti en ")+4]
    if(tmp_year.isnumeric()):
        year = tmp_year
    return year


# Get name in webpage and apply filters for irrelevant informations
def get_human_names(text, filter):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""

    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if(len(person) > 1): # Check if we have name + surname

            for part in person:
                name += part + ' '

            if(name[-1] == " "):
                name = name[:-1]

            ## TODO : Trouver meilleure façon de faire et plus generique
            # Multiple name for a same person
            if("Roll" in name and "Morton" in name):
                name = "Roll Morton"

            elif ("Chuck" in name and "Rio" in name):
                name = "Danny Flores"

            elif ("Harold" in name and "Bailey" in name):
                name = "Michael Bailey"

            elif ("Art" in name and "Taylor" in name):
                name = "Art Taylor"

            elif("Frank" in name and "Thomas" in name):
                name = "Franck Thomas"

            elif( name == "James Stanley Hall"):
                name = "Jim Hall"

            elif( name == "Benjamin A. Riley"):
                name = "Ben Riley"

            elif( name == "Dewey Walter Redman"):
                name = "Dewey Redman"

            elif( name == "Lovella May Borg"):
                name = "Carla Bley"

            elif( name == "Kenny Kirkland"):
                name = "Kenneth David Kirkland"

            elif( name == "Benny Bailey"):
                name = "Ernest Harold Bailey"

            elif( name == "John Tchicai"):
                name = "John Martin Tchicai"

            if(name not in person_list):
                # Avoid producers, journalist, song-writer, song engineer, labels, ...
                canbeadd = True
                for forbword in filter:
                    if(unidecode.unidecode(forbword).lower() in unidecode.unidecode(name).lower() or unidecode.unidecode(forbword).lower() == unidecode.unidecode(name).lower()):
                        canbeadd = False
                        break
                if(canbeadd):
                    person_list.append(name)

            name = ''
        person = []
    res = ""
    for pers in person_list:
        res += pers + ","
    return (res[:-1])



if __name__ == '__main__':
    main()
