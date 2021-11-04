import network as n
import data_parser as p

"""
# OUTPUT : FESTIVAL
==========================================
Clustering coefficient :  0.9204529908238623
Transitivity value :  0.7131485284798672
Number of community :  1166
Total number of nodes :  13796
Average degree :  70.67226890756302
==========================================
List of most connected nodes and their degree :
David Sanborn 13  :  152
Steve Ferrone 13  :  161
Patti Austin 12  :  169
Chaka Khan 10  :  187
Claude Nobs 11  :  211
Herbie Hancock 14  :  212
Nathan East 11  :  218
Toots Thielemans 16  :  220
George Duke 11  :  276
Quincy Jones 12  :  280
==========================================

# OUTPUT : Disque Wikipedia
==========================================
Clustering coefficient :  0.8322086688639141
Transitivity value :  0.6195193487564721
Number of community :  128
Total number of nodes :  1573
Average degree :  29.833333333333332
==========================================
List of most connected nodes and their degree :
Quentin Jackson  :  41
Cootie Williams  :  42
Elvin Jones  :  42
Ernie Royal  :  44
John Swenson  :  44
Ray Nance  :  45
Harry Carney  :  45
Ron Carter  :  45
Ben Webster  :  47
John Lewis  :  47
Johnny Coles  :  48
Miles Davis  :  50
George Russell  :  50
Sonny Rollins  :  51
Roy Eldridge  :  55
Barney Bigard  :  57
Eric Dolphy  :  58
Johnny Griffin  :  60
Johnny Hodges  :  74
Duke Ellington  :  154
==========================================
"""


def main():
    G = n.Network()

    #lst_data_set = ["../data/data.csv", "../data/data2.csv","../data/data3.csv","../data/data4.csv", "../data/data5.csv", "../data/data6.csv", "../data/data7.csv"]
    #lst_data_set = ["../data/rap_belge.csv"]
    #lst_data_set = ["../data/ex.csv"]
    #lst_data_set = ["../data/data7c.csv"]
    lst_data_set = ["../data/data7c.csv",
                    "../data/data8c.csv",
                    "../data/data9c.csv",
                    "../data/data10c.csv",
                    "../data/data11c.csv",
                    "../data/data12c.csv",
                    "../data/data13c.csv",
                    "../data/data14c.csv",
                    "../data/data15c.csv",
                    "../data/data16c.csv",
                    "../data/data17c.csv",
                    ]
    """
    lst_data_set = ["../data/data7.csv",
                    "../data/data8.csv",
                    "../data/data9.csv",
                    "../data/data10.csv",
                    "../data/data11.csv",
                    "../data/data12.csv",
                    "../data/data13.csv",
                    "../data/data14.csv",
                    "../data/data15.csv",
                    "../data/data16.csv",
                    "../data/data17.csv",
                    "../data/data18.csv",
                    "../data/data19.csv",
                    "../data/data20.csv",
                    "../data/data21.csv",
                    "../data/data22.csv",
                    "../data/data23.csv",
                    "../data/data24.csv",
                    "../data/data25.csv",
                    "../data/data26.csv",
                    "../data/data27.csv",
                    "../data/data28.csv",
                    "../data/data29.csv",
                    "../data/data30.csv",
                    "../data/data31.csv",
                    "../data/data32.csv",
                    "../data/data33.csv",
                    "../data/data34.csv",
                    "../data/data35.csv",
                    "../data/data36.csv",
                    "../data/data37.csv",
                    "../data/data38.csv",
                    "../data/data39.csv",
                    "../data/data40.csv",
                    "../data/data41.csv",
                    "../data/data42.csv",
                    "../data/data43.csv",
                    "../data/data44.csv",
                    "../data/data45.csv",
                    "../data/data46.csv",
                    "../data/data47.csv",
                    "../data/data48.csv",
                    "../data/data49.csv",
                    "../data/data50.csv",
                    "../data/data51.csv",
                    "../data/data52.csv",
                    "../data/data53.csv",
                    "../data/data54.csv",
                    "../data/data55.csv",
                    "../data/data56.csv",
                    "../data/data57.csv",
                    "../data/data58.csv",
                    "../data/data59.csv",
                    "../data/data60.csv",
                    "../data/data61.csv",
                    "../data/data62.csv",
                    "../data/data63.csv",
                    "../data/data64.csv",
                    "../data/data65.csv",
                    "../data/data66.csv",
                    "../data/data67.csv",
                    "../data/data68.csv",
                    "../data/data69.csv",
                    "../data/data70.csv",
                    "../data/data71.csv",
                    "../data/data72.csv",
                    "../data/data73.csv",
                    "../data/data74.csv",
                    "../data/data75.csv",
                    "../data/data76.csv",
                    "../data/data77.csv",
                    "../data/data78.csv",
                    "../data/data79.csv",
                    "../data/data80.csv",
                    "../data/data81.csv",
                    "../data/data82.csv",
                    "../data/data83.csv",
                    "../data/data84.csv",
                    "../data/data85.csv",
                    "../data/data86.csv",
                    "../data/data87.csv",
                    "../data/data88.csv",
                    "../data/data89.csv",
                    "../data/data90.csv",
                    "../data/data91.csv",
                    "../data/data92.csv",
                    "../data/data93.csv",
                    "../data/data94.csv",
                    "../data/data95.csv",
                    "../data/data96.csv",
                    "../data/data97.csv",
                    ]
    """



    print('==========================================')

    print('1.1 - Merging data sets and creating datastructure')
    dic_mus_collab, dic_mus_year_collab = merge_datasets(lst_data_set)
    #print('1.2 - Sorting data sets.')
    #dic_mus_collab, dic_mus_year_collab = sort_dict_by_year(dic_mus_collab, dic_mus_year_collab)


    print('2 - Building nodes.')
    dic_instru_mus = create_node(dic_mus_collab, G)


    print('2 - Instrument network.')

    # TODO : Afficher le réseau d'instruments
    """
    G2 = n.Network()
    create_node(dic_instru_mus, G2)
    pds2 = comput_weight(dic_instru_mus, G2)
    create_edge(dic_instru_mus, pds2, G2)
    G2.show_network(False, False)
    """
    #print('2.2 - Creating musicians data sets.')
    #G.create_csv_musician()

    print('3.1 - Building weighted edges.')
    pds = comput_weight(dic_mus_collab, G)
    create_edge(dic_mus_collab, pds, G)

    #print('3.2 - Building dynamic edges.')
    #create_dynamic_edge(dic_mus_collab, G, dic_mus_year_collab)

    print('4 - Drawing.')
    #G.show_network(False, False)

    G.show_community(False) # ouvrir le fichier, pas juste previsu
    #G.show_occurence()
    #G.show_clustering()
    #G.get_gamma_value()
    #G.show_rich_club_distrib()
    #G.show_distrib_pk()
    #G.show_dynamic_network(dic_mus_year_collab, False)

    print('==========================================')
    G.printInfo(20, False, False)
    #G.printInfoDyna(dic_mus_year_collab)
    print('==========================================')

#================================================================================
## TODO : move these two fun to new 'utility' class

# Sort musician collab dict the same order than musician year dict
def sort_dict_by_year(dic_mus_collab, dic_mus_year_collab):
    new_dict_mus_collab = {}
    dic_mus_year_collab = {k: v for k, v in sorted(dic_mus_year_collab.items(), key=lambda item: item[1])}
    for key in dic_mus_year_collab:
        new_dict_mus_collab[key] = dic_mus_collab[key]

    return new_dict_mus_collab, dic_mus_year_collab


# Combine the different dict create from the different dataset
# And return 2 dict {album:year} and {album: lst_musician+(instrument)}
def merge_datasets(lst_data_set):
    dic_mus_collab = {}
    dic_mus_year_collab = {}
    dic_mus_instrument = {}
    for dataset in lst_data_set:
        P = p.Parser(dataset)
        P.parse_csv()

        dic_mus_collab_tmp = P.get_dict_musician_alb()
        dic_mus_collab.update(dic_mus_collab_tmp)

        dic_mus_year_collab_tmp = P.get_dict_year()
        dic_mus_year_collab.update(dic_mus_year_collab_tmp)

    return dic_mus_collab, dic_mus_year_collab


#================================================================================
## TODO Move to network class

## TODO : must be OPTIMIZE

# Create all the node
def create_node(dic_alb_musician, G):
    dic_instru_mus = {}
    for k in dic_alb_musician:
        for musician in dic_alb_musician[k]:
            if(musician != "" and musician != " " and len(musician) > 2):
                if("(" in musician):
                    muscian_data = musician.split("(")
                    musician_name = muscian_data[0]
                    musician_instru = muscian_data[1][:-1]

                    instrument = "unknown"
                    if(musician_instru.lower() in ["bass", "b", "bas", "ba", "double bass", "basse"]):
                        instrument = "bass"
                    if(musician_instru.lower() in ["artist", "vocalist", "vocal", "voc", "voca", "vocals", "lead vocals", "vo", "chant", "MC", "choriste", "backing vocals", "backvocals", "back voc", "singer"]):
                        instrument = "vocal"
                    if(musician_instru.lower() in ["batterie", "percu", "percussion", "d", "drums", "per", "dr"]):
                        instrument = "drum"
                    if(musician_instru.lower() in ["guitar", "g", "guitare", "guitars", "guit", "guita"]):
                        instrument = "guitar"
                    if(musician_instru.lower() in ["piano", "keyboards", "keyboard", "claviers", "kbds", "ke", "keys", "p", "k"]):
                        instrument = "piano/clavier"
                    if(musician_instru.lower() in ["trombon", "trombone"]):
                        instrument = "trombon"
                    if(musician_instru.lower() in ["violin", "violon", "viola", "1st violin", "2nd violin"]):
                        instrument = "violin"
                    if(musician_instru.lower() in ["cello", "cell"]):
                        instrument = "cello"
                    if(musician_instru.lower() in ["flut", "flute"]):
                        instrument = "flut"
                    if(musician_instru.lower() in ["dj", "sampler", "turntables", "turntable", "laptop/ad", "laptop"]):
                        instrument = "dj/laptop/sampler"
                    if(instrument not in dic_instru_mus):
                        dic_instru_mus[instrument] = [musician_name]
                    else:
                        dic_instru_mus[instrument].append(musician_name)

                else:
                    musician_name = musician
                if("&amp;" in musician_name):
                    #replace par &
                    pass
                #print(musician_name)
                G.addnode(musician_name)
    return dic_instru_mus

## TODO : must be OPTIMIZE

# Build edges between nodes
def create_edge(dic_alb_musician, dict_pds, G):
    for k in dic_alb_musician:
        for kk in dic_alb_musician:
            if(k != kk):
                for musician in dic_alb_musician[k]:
                    for musician2 in dic_alb_musician[k]:
                        if(musician != musician2):
                            if(musician != "" and musician != " " and len(musician) > 2):
                                if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                    if("(" in musician):
                                        muscian_data = musician.split("(")
                                        musician_name = muscian_data[0]
                                    else:
                                        musician_name = musician
                                    if("(" in musician2):
                                        muscian2_data = musician2.split("(")
                                        musician2_name = muscian2_data[0]
                                    else:
                                        musician2_name = musician2
                                    G.addedgeweight(musician_name, musician2_name, dict_pds[musician][musician2])

## TODO : must be OPTIMIZE

def create_dynamic_edge(dic_alb_musician, G, dic_mus_year_collab):
    for k in dic_alb_musician:
        for kk in dic_alb_musician:
            if(k != kk):
                if(str(dic_mus_year_collab[k]).isnumeric()):
                    time = int(dic_mus_year_collab[k])
                    for musician in dic_alb_musician[k]:
                        for musician2 in dic_alb_musician[k]:
                            if(musician != musician2):
                                if(musician != "" and musician != " " and len(musician) > 2):
                                    if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                        G.adddynedge(musician, musician2, time)

## TODO : must be OPTIMIZE

# Compute weight of edge between musician
def comput_weight(dict_alb_musician, G):
    dic_all_musician_tmp = {}
    for k in dict_alb_musician:
        for musician in dict_alb_musician[k]:
            if(musician not in dic_all_musician_tmp):
                dic_all_musician_tmp[musician] = 0
    dic_all_musician = {}
    for mus in dic_all_musician_tmp:
        dic_all_musician[mus] = dic_all_musician_tmp.copy()
    for alb in dict_alb_musician:
        for musician in dict_alb_musician[alb]:
            for ms in dict_alb_musician[alb]:
                if(ms != musician):
                    dic_all_musician[musician][ms] += 1
    return dic_all_musician


if __name__ == '__main__':
    main()

# https://www.overleaf.com/project/6033b2143f7784b3213378d4
