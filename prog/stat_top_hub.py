import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def main():
    #path = "../data/q1_q2_hub.csv"
    path = "../data/top_hub.csv"

    dict_label = parse_data(path, -3)
    dict_label_occ = count_data(dict_label)
    lst_x, lst_y = dict_to_lst(dict_label_occ)
    print(len(dict_label_occ))
    show_data("Label","Count", lst_x, lst_y)

    dict_style = parse_data(path, -2)
    dict_style_occ = count_data(dict_style)
    lst_x, lst_y = dict_to_lst(dict_style_occ)
    show_data("Genre","Count", lst_x, lst_y)

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
    plt.barh(lst_x, lst_y)
    plt.xlabel(y_label, fontsize=12)
    plt.ylabel(x_label, fontsize=12)
    plt.yticks(fontsize=7)
    fig.savefig('top_hub_stat.png')
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
