import data_parser as p
from ethnicolr import census_ln, pred_census_ln
import csv

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

        if(musician_instru.lower() in ["bass", "b", "b.", "bas", "electric bas", "electric bass", "acoustic bass", "ba", "bs", "double bass", "basse"]):
            instrument = "bass"
        elif(musician_instru.lower() in ["artist", "lead vo", "all voc", "v", "vocalist", "vocal", "voice", "voc.", "voc", "ld voc", "bk voc", "voca", "vocals", "lead vocals", "lead voc", "vo", "chant", "mc" , "m", "choriste", "backing vocals", "backing vocal", "backvocals", "back voc", "singer", "rap", "lead rap"]):
            instrument = "vocal"
        elif(musician_instru.lower() in ["batterie", "d", "drums", "drum", "dru", "dr", "steel dr", "jamaica drums"]):
            instrument = "drum"
        elif(musician_instru.lower() in ["talking dr", "percu", "timbals", "tim", "bells", "percus", "percussion", "percussi", "percussio", "percussionist", "percussions", "perc.", "per", "perc"]):
            instrument = "percussion"
        elif(musician_instru.lower() in ["elg", "cg", "guitar", "gu", "gui", "bjo", "g", "guitare", "guitars", "guit", "guit.", "guita"]):
            instrument = "guitar"
        elif(musician_instru.lower() in ["uk"]):
            instrument = "ukulele"
        elif(musician_instru.lower() in ["elp", "piano", "pf", "p.", "pian", "p"]):
            instrument = "piano"
        elif(musician_instru.lower() in ["synth", "keyboards", "keyboard", "key", "keyb", "kb", "claviers", "kbds", "kbd", "ke", "keys", "k"]):
            instrument = "keyboard"
        elif(musician_instru.lower() in ["trombon", "trombone", "tb"]):
            instrument = "trombon"
        elif(musician_instru.lower() in ["vl", "vn", "violin", "violon", "viola", "1st violin", "2nd violin", "1st violi", "2nd violi", "vln", "alto violin", "fiddle"]):
            instrument = "violin"
        elif(musician_instru.lower() in ["vc", "cello", "cell"]):
            instrument = "cello"
        elif(musician_instru.lower() in ["tuba"]):
            instrument = "tuba"
        elif(musician_instru.lower() in ["flut", "flute", "fl", "pc"]):
            instrument = "flut"
        elif(musician_instru.lower() in ["french horn", "frh", "horn", "horns"]):
            instrument = "french horn"
        elif(musician_instru.lower() in ["clarinet", "oboe", "o", "cl", "fg", "faggoto", "ob"]):
            instrument = "clarinet"
        elif(musician_instru.lower() in ["bassoon"]):
            instrument = "bassoon"
        elif(musician_instru.lower() in ["organ", "hammond organ", "or"]):
            instrument = "organ"
        elif(musician_instru.lower() in ["tub", "tuba"]):
            instrument = "tuba"
        elif(musician_instru.lower() in ["trumpet", "tr", "trumpe", "t", "tp", "tp."]):
            instrument = "trumpet"
        elif(musician_instru.lower() in ["s", "s.", "ss", "ss.", "ts", "ts.", "as", "as.", "bs", "bs.", "sax", "saxe", "saxes", "saxophone", "saxophon", "sa", "saxo", "baritone sax", "tenor sax", "tenor sa", "alto sax", "tenor saxophone", "baritone saxophone", "bar"]):
            instrument = "saxophone"
        elif(musician_instru.lower() in ["hca", "hc","harmonica", "harmonic"]):
            instrument = "harmonica"
        elif(musician_instru.lower() in ["bandoneon"]):
            instrument = "bandoneon"
        elif(musician_instru.lower() in ["accordio", "accordion", "pac",  "acc.", "acc"]):
            instrument = "accordion"
        elif(musician_instru.lower() in ["n'goni"]):
            instrument = "n'goni"
        elif(musician_instru.lower() in ["dj", "sampler", "turntab", "turntabl", "turntables", "tabl", "turntable", "laptop/ad", "laptop"]):
            instrument = "dj/laptop"
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

    # Create a database with all the informations on a musician
    def create_csv_musician(self, network):
        dict_alb_musician = dict(network.getgraph().degree)
        path = "../data/"
        name = path + "muscians.csv"
        file = open(name, 'w', newline='')
        spamWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        lst_mus = []
        for musician in dict_alb_musician:
            line_in_csv = [musician]

            mus = musician.split(' ')
            sex = self.GenderD.get_gender(mus[0])
            line_in_csv.append(sex)

            line_in_csv.append("date de naissance")
            line_in_csv.append("instrument")
            line_in_csv.append("country")

            # Get ethnicity with Tensor Flow
            names = [{'name': mus[0]}]
            df = pd.DataFrame(names)
            ethnicity = census_ln(df, 'name').values.tolist()
            eth = "None"
            if("nan" not in ethnicity[0][1:]):
                ethn_pourc = max(ethnicity[0][1:])
                ind = ethnicity[0].index(ethn_pourc)
                if(ind == 1):
                    eth = "White"
                if(ind == 2):
                    eth = "Black"
                if(ind == 3):
                    eth = "API"
                if(ind == 4):
                    eth = "AIAN"
                if(ind == 5):
                    eth = "2PRACE"
                if(ind == 6):
                    eth = "Hispanic"
            line_in_csv.append(eth)

            if(musician not in lst_mus):
                spamWriter.writerow(line_in_csv)
                lst_mus.append(musician)
