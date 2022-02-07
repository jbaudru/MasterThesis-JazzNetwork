import data_parser as p
from itertools import islice
import csv
import unidecode

class Utility:
    def __init__(self):
        pass

    def get_name_and_instru(self, musician_dt):
        if("(" in musician_dt):
            muscian_data = musician_dt.split("(")
            musician_name = muscian_data[0]
            musician_instru = muscian_data[1][:-1]
        else:
            musician_name = musician_dt
            musician_instru = "unknown"
        return musician_name, musician_instru


    def clean_musician_name_unicode(self, musician_name):
        if("&amp;" in musician_name):
            ind = musician_name.index("&amp;")
            musician_name = musician_name[:ind] + "&" + musician_name[ind+5:]
        return musician_name

    def filter_instrument(self, musician_instru):
        if(len(musician_instru)>1 and ')' in musician_instru):
            ind = musician_instru.index(")")
            musician_instru = musician_instru[:ind]

        if("/" in musician_instru):
            musician_instru = musician_instru.split("/")[0]
        instrument = "unknown"

        if(musician_instru.lower() in ["bass", "b", "b.", "contrebasse", "bas", "electric bas", "electric bass", "acoustic bass", "ba", "bs", "double bass", "basse"]):
            instrument = "Bass"
        elif(musician_instru.lower() in ["artist", "lead vo", "all voc", "v", "vocalist", "vox", "choeur", "vocal", "voice", "voc.", "voc", "ld voc", "bk voc", "voca", "vocals", "lead vocals", "lead voc", "vo", "chant", "mc" , "m", "choriste", "backing vocals", "backing vocal", "backvocals", "back voc", "singer", "rap", "lead rap"]):
            instrument = "Vocal"
        elif(musician_instru.lower() in ["batterie", "d", "drums", "drum", "dru", "dr", "steel dr", "jamaica drums"]):
            instrument = "Drum"
        elif(musician_instru.lower() in ["talking dr", "percu", "timbals", "tim", "bells", "percus", "percussion", "percussi", "percussio", "percussionist", "percussions", "perc.", "per", "perc"]):
            instrument = "Percussion"
        elif(musician_instru.lower() in ["elg", "cg", "guitar", "gu", "gui", "bjo", "g" ,"g.", "guitare", "guitars", "guit", "guit.", "guita"]):
            instrument = "Guitar"
        elif(musician_instru.lower() in ["uk"]):
            instrument = "Ukulele"
        elif(musician_instru.lower() in ["elp", "piano", "pf", "p.", "pian", "p", "el-p"]):
            instrument = "Piano"
        elif(musician_instru.lower() in ["synth", "keyboards", "keyboard", "key", "keyb", "kb", "claviers", "kbds", "kbd", "ke", "keys", "k", "k."]):
            instrument = "Keyboard"
        elif(musician_instru.lower() in ["trombon", "trombone", "trombones", "tb", "trumbone", "1st trombone", "2nd trombone"]):
            instrument = "Trombon"
        elif(musician_instru.lower() in ["vl", "vn", "violin", "violon", "viola", "1st violin", "2nd violin", "1st violi", "2nd violi", "vln", "alto violin", "fiddle"]):
            instrument = "Violin"
        elif(musician_instru.lower() in ["vc", "cello", "cell"]):
            instrument = "Cello"
        elif(musician_instru.lower() in ["tuba"]):
            instrument = "Tuba"
        elif(musician_instru.lower() in ["flut", "flute", "fl", "pc"]):
            instrument = "Flut"
        elif(musician_instru.lower() in ["french horn", "frh", "horn", "horns", "frenchh"]):
            instrument = "French Horn"
        elif(musician_instru.lower() in ["clarinet", "oboe", "o", "cl", "fg", "faggoto", "ob"]):
            instrument = "Clarinet"
        elif(musician_instru.lower() in ["bassoon"]):
            instrument = "Bassoon"
        elif(musician_instru.lower() in ["organ", "hammond organ", "or"]):
            instrument = "Organ"
        elif(musician_instru.lower() in ["tub", "tuba"]):
            instrument = "Tuba"
        elif(musician_instru.lower() in ["trumpet", "tr", "tr.", "trumpe", "t", "tp", "tp."]):
            instrument = "Trumpet"
        elif(musician_instru.lower() in ["s", "s.", "ss", "ss.", "ts", "ts.", "as", "as.", "bs", "bs.", "sax", "saxe", "saxes", "saxophone", "saxophon", "sa", "saxo", "baritone sax", "tenor sax", "tenor sa", "alto sax", "tenor saxophone", "baritone saxophone", "bar"]):
            instrument = "Saxophone"
        elif(musician_instru.lower() in ["hca", "hc","harmonica", "harmonic"]):
            instrument = "Harmonica"
        elif(musician_instru.lower() in ["bandoneon"]):
            instrument = "Bandoneon"
        elif(musician_instru.lower() in ["accordio", "accordion", "pac",  "acc.", "acc"]):
            instrument = "Accordion"
        elif(musician_instru.lower() in ["n'goni"]):
            instrument = "N'goni"
        elif(musician_instru.lower() in ["dj", "sampler", "turntab", "turntabl", "turntables", "tabl", "turntable", "laptop/ad", "laptop"]):
            instrument = "DJ"
        elif(musician_instru.lower() in ["conductor", "cond"]):
            instrument = "Conductor"
        elif(musician_instru.lower() in ["harp"]):
            instrument = "Harp"
        """
        else:
            if(musician_instru.lower() != "" and musician_instru.lower() != "unknown"):
                print(musician_instru.lower())
        """
        return instrument

    # And return 2 dict {album:year} and {album: lst_musician+(instrument)}
    def get_dic_from_datasets(self, dataset):
        dic_mus_collab = {}
        dic_mus_year_collab = {}
        P = p.Parser(dataset)
        P.parse_csv()
        dic_mus_collab_tmp = P.get_dict_musician_alb()
        dic_mus_collab.update(dic_mus_collab_tmp)
        dic_mus_year_collab_tmp = P.get_dict_year()
        dic_mus_year_collab.update(dic_mus_year_collab_tmp)
        return dic_mus_collab, dic_mus_year_collab

    # Sort musician collab dict the same order than musician year dict
    def sort_dict_by_year(self, dic_mus_collab, dic_mus_year_collab):
        new_dict_mus_collab = {}
        dic_mus_year_collab = {k: v for k, v in sorted(dic_mus_year_collab.items(), key=lambda item: item[1])}
        for key in dic_mus_year_collab:
            new_dict_mus_collab[key] = dic_mus_collab[key]
        return new_dict_mus_collab, dic_mus_year_collab

    # Special function for the neworlean dataset
    # convert the raw data get from the website (comma)
    # to data set in the format use in this project (semicolon)
    def csv_comma_to_semicolon(self, csv_input, csv_output):
        # Band name, Year, Musicians
        file = open(csv_input, "r")
        file_out = open(csv_output, 'w')
        spamWriter = csv.writer(file_out, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        for line in file:
            tmp_lst=[]
            lsttmp = line.split(",")
            endline = False
            lst_musician = []
            # For each
            if(len(lsttmp) != 1): # Avoid empty data
                for elem in lsttmp:
                    if(self.is_date(elem)):
                        year = elem.split("-")[0]
                        endline = True
                    else:
                        if(endline == False):
                            lst_musician.append(elem)
                        else:
                            break
            if(len(lst_musician)> 0):
                str_musician = ""
                # handle AND,FEAT case to add to the list
                # filter name
                for i in range(0,len(lst_musician)):
                    if(i < len(lst_musician)-1):
                        str_musician += lst_musician[i] + ","
                    else:
                        str_musician += lst_musician[i]
                    str_musician = str_musician.replace(" and ", "")
                    str_musician = str_musician.replace(" feat.", ",")
                    str_musician = str_musician.replace(" featuring ", ",")
                    str_musician = str_musician.replace(" with ", ",")
                    str_musician = str_musician.replace(" & ", ",")
                    str_musician = str_musician.replace(" + ", ",")
                    str_musician = str_musician.replace("\"", "")
                    str_musician = str_musician.replace(" with guests ", ",")
                    if(str_musician[0] == "\""):
                        print("PROBLEM")

                print(str_musician)

                title = lst_musician[0].upper()
                tmp_lst.append(title)  # Alb name
                tmp_lst.insert(1, year)
                tmp_lst.insert(2, "label")
                tmp_lst.insert(3, str_musician)
                spamWriter.writerow(tmp_lst)


    def is_date(self, string, fuzzy=False):
        if(string.count("-")==2):
            return True
        else:
            return False

    # Create a database with all the informations on a musician
    def create_csv_musician(self, network, name, tophub = False, n = None):
        d = dict(network.getgraph().degree)
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])} # Sort dict in order way
        if(tophub and n != None):
            d = dict(list(d.items())[-n:])
        elif(not tophub and n != None): # q1 and q2
            d = dict(list(d.items())[len(d)//4:len(d)//2])
            d = list(islice(d.items(), n))
        path = "../data/"
        name = path + name + ".csv"
        file = open(name, 'w', newline='')
        spamWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        lst_mus = []
        for musician in d:
            if(not tophub):
                deg = musician[1]
                musician = musician[0]
            else:
                deg = d[musician]
            line_in_csv = [musician]

            line_in_csv.append("date de naissance")
            line_in_csv.append("instrument")
            line_in_csv.append("country")

            line_in_csv.append(deg) # degree

            if(musician not in lst_mus):
                spamWriter.writerow(line_in_csv)
                lst_mus.append(musician)
