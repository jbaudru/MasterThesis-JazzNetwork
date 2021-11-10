import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def main():
    #path = "../data/q1-q2_montreux.csv"
    #path = "../data/q1-q2_wiki.csv"
    #path = "../data/top_hub_montreux.csv"
    path = "../data/top_hub_wiki.csv"

    data= parse_data(path, -1)
    dict_label_occ = count_data(data)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("City","Count", lst_x, lst_y)

    data= parse_data(path, -2)
    dict_label_occ = count_data(data)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("Sex","Count", lst_x, lst_y)

    data= parse_data(path, -4)
    dict_label_occ = count_data(data)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("Country","Count", lst_x, lst_y)

    data= parse_data(path, -5)
    dict_label_occ = count_data(data)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("Instrument","Count", lst_x, lst_y)

    data= parse_data(path, -6)
    dict_label_occ = count_data(data)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("Year","Count", lst_x, lst_y)
    sum_year = 0
    for i in range(0,len(lst_x)):
        sum_year += int(lst_x[i])
    print("Average birth year : ", sum_year/len(lst_x))


def count_data(dict):
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


def dict_to_lst(dict):
    lst_x = []
    lst_y = []
    for elem in dict:
        lst_x.append(elem)
        lst_y.append(dict[elem])
    return lst_x, lst_y


def show_data(x_label, y_label, lst_x, lst_y):
    fig = plt.figure()

    colors =  plt.cm.tab20c( (4./3*np.arange(20*3/4)).astype(int) )
    colors = colors.tolist()[:len(lst_y)]

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
    plt.yticks(fontsize=7)
    #fig.savefig('top_hub_stat.png')
    plt.show()


def parse_data(path, index):
    file = open(path, "r")
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


if __name__ == "__main__":
    main()
