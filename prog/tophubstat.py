import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class TopHubStat:
    def __init__(self, path=None):
        self.path = path

    def getdictCity(self):
        return self.parse_data(-1)

    def getdictSex(self):
        return self.parse_data(-2)

    def getdictCountry(self):
        return self.parse_data(-4)

    def getdictInstru(self):
        return self.parse_data(-5)

    def getdictYear(self):
        return self.parse_data(-6)

    def showCity(self):
        dict_label_occ = self.count_data(self.getdictCity())
        lst_x, lst_y = self.dict_to_lst(dict_label_occ)
        ind_to_del = lst_x.index("\n")
        lst_x.pop(ind_to_del)
        lst_y.pop(ind_to_del)
        self.show_data("City","Count", lst_x, lst_y)

    def showSex(self):
        dict_label_occ = self.count_data(self.getdictSex())
        lst_x, lst_y = self.dict_to_lst(dict_label_occ)
        #lst_x = ["Male"]
        self.show_data("Sex","Count", lst_x, lst_y)

    def showCountry(self):
        dict_label_occ = self.count_data(self.getdictCountry())
        lst_x, lst_y = self.dict_to_lst(dict_label_occ)
        nw_lst_x = []
        for country in lst_x:
            if(country == "Allemagne"):
                nw_lst_x.append("Germany")
            elif(country == "Suède"):
                nw_lst_x.append("Sweden")
            elif(country == "Jamaique"):
                nw_lst_x.append("Jamaica")
            elif(country == "Belgique"):
                nw_lst_x.append("Belgium")
            elif(country == "Suisse"):
                nw_lst_x.append("Switzerland")
            elif(country == "Angleterre"):
                nw_lst_x.append("England")
            else:
                nw_lst_x.append(country)
        self.show_data("Country","Count", nw_lst_x, lst_y)

    def showInstru(self):
        dict_label_occ = self.count_data(self.getdictInstru())
        lst_x, lst_y = self.dict_to_lst(dict_label_occ)
        self.show_data("Instrument","Count", lst_x, lst_y)

    def showYear(self):
        dict_label_occ = self.count_data(self.getdictYear())
        lst_x, lst_y = self.dict_to_lst(dict_label_occ)
        self.show_data("Year","Count", lst_x, lst_y)

    def count_data(self, dict):
        data_counter = {}
        for item in dict:
            for elem in dict[item]:
                if(elem[-1] == " "):
                    elem = elem[:-1]
                if(elem not in data_counter):
                    data_counter[elem] = 1
                else:
                    data_counter[elem] += 1
        data_counter = {k: v for k, v in sorted(data_counter.items(), key=lambda item: item[1])}
        return data_counter


    def dict_to_lst(self, dict):
        lst_x = []
        lst_y = []
        for elem in dict:
            lst_x.append(elem)
            lst_y.append(dict[elem])
        return lst_x, lst_y


    def show_data(self, x_label, y_label, lst_x, lst_y):
        #fig = plt.figure()


        colors =  plt.cm.tab20c( (4./3*np.arange(20*3/4)).astype(int) )
        colors = colors.tolist()[:len(lst_y)][::-1]
        """
        nw_col = []
        for i in range(0, len(colors)):
            tuple = (colors[i][0], colors[i][1], colors[i][2], colors[i][3])
            nw_col.append(tuple)

        nw_col += nw_col
        nw_col = nw_col[:len(lst_y)]

        plt.style.use('seaborn-dark')
        plt.barh(lst_x, lst_y, color=colors)
        plt.xlabel(y_label, fontsize=10)
        plt.ylabel(x_label, fontsize=10)
        plt.yticks(fontsize=5)
        #fig.savefig('top_hub_stat.png')
        """
        #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        explode = [0 for i in range(0,len(lst_y))]
        fig1, ax1 = plt.subplots()
        wedges, texts, autotexts = ax1.pie(lst_y, explode=explode, labels=lst_x, colors=colors, autopct='%1.1f%%', pctdistance=0.9, rotatelabels=True, labeldistance=1, textprops=dict(color="black", size=8), shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #ax1.legend(wedges, lst_x, title=x_label, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.show()


    def parse_data(self, index):
        file = open(self.path, "r")
        dict_musician_multival = {}
        cnt_line = 0
        for line in file:
            cnt_line+=1
            if(cnt_line>1):
                lsttmp = line.split(";")
                if(len(lsttmp) != 1): # Avoid empty data
                    lst_multival_data = lsttmp[index].split(",")
                    lst_multival_data_clean = []
                    for elem in lst_multival_data:
                        if elem != "":
                            if(elem[0] == ' '):
                                lst_multival_data_clean.append(elem[1:])
                            else:
                                lst_multival_data_clean.append(elem)
                    if(lsttmp[0] != '' and lst_multival_data[0] != ''):

                        dict_musician_multival[lsttmp[0]] = lst_multival_data_clean
        return dict_musician_multival
