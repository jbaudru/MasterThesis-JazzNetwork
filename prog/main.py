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

    lst_data_set_album = ["../data/data.csv", "../data/data2.csv","../data/data3.csv","../data/data4.csv", "../data/data5.csv", "../data/data6.csv"]
    
    lst_data_set_montreux = []
    for i in range(7, 10):
        filename = "../data/data" + str(i) + "c.csv"
        lst_data_set_montreux.append(filename)


    print('==========================================')

    print('1.1 - Merging data sets and creating datastructure')
    dic_mus_collab, dic_mus_year_collab = merge_datasets(lst_data_set_montreux)
    #print('1.2 - Sorting data sets.')
    #dic_mus_collab, dic_mus_year_collab = sort_dict_by_year(dic_mus_collab, dic_mus_year_collab)


    print('2 - Building nodes.')
    create_node(dic_mus_collab, G)
    
    #print('2.2 - Creating musicians data sets.')
    #G.create_csv_musician()

    print('3.1 - Building weighted edges.')
    pds = comput_weight(dic_mus_collab, G)
    dic_instru_mus = create_edge(dic_mus_collab, pds, G, True)
    
    print("test instru réseau")
    H = n.Network(True)
    create_node(dic_instru_mus, H)
    pds2 = comput_weight_instru(dic_instru_mus, H)
    
    create_edge_instru(dic_instru_mus, pds2, H)
    H.show_network(True, True)
    #print('3.2 - Building dynamic edges.')
    #create_dynamic_edge(dic_mus_collab, G, dic_mus_year_collab)

    print('4 - Drawing.')
    #H.show_network(False, False)
    #G.show_network(False, True)
    #G.show_community(False) # ouvrir le fichier, pas juste previsu
    #G.show_occurence()
    #G.show_clustering()
    #G.get_gamma_value()
    #G.show_rich_club_distrib()
    #G.show_distrib_pk()
    #G.show_dynamic_network(dic_mus_year_collab, False)

    print('==========================================')
    #G.printInfo(20, False, False)
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
                
                musician_name, musician_instru = get_name_and_instru(musician)
                musician_name = clean_musician_name_unicode(musician_name)
                                    
                if("(" not in musician_name and ")" not in musician_name):
                    G.addnode(musician_name)
                    

    


def get_name_and_instru(musician_dt):
    if("(" in musician_dt):
        muscian_data = musician_dt.split("(")
        musician_name = muscian_data[0]
        musician_instru = muscian_data[1][:-1]
    else:
        musician_name = musician_dt
        musician_instru = "unknown"
    return musician_name, musician_instru


def clean_musician_name_unicode(musician_name):
    if("&amp;" in musician_name):
        ind = musician_name.index("&amp;")
        musician_name = musician_name[:ind] + "&" + musician_name[ind+5:]
    return musician_name


def filter_instrument(musician_instru):
    if(len(musician_instru)>1 and ')' in musician_instru):
        ind = musician_instru.index(")")
        musician_instru = musician_instru[:ind]
                
    instrument = "unknown"
    if(musician_instru.lower() in ["bass", "b", "bas", "ba", "bs", "double bass", "basse"]):
        instrument = "bass"
    if(musician_instru.lower() in ["artist", "vocalist", "vocal", "voc.", "voc", "ld voc", "bk voc", "voca", "vocals", "lead vocals", "vo", "chant", "MC", "choriste", "backing vocals", "backvocals", "back voc", "singer"]):
        instrument = "vocal"
    if(musician_instru.lower() in ["batterie", "percu", "percussion", "d", "drums", "per", "perc", "dr", "steel dr"]):
        instrument = "drum"
    if(musician_instru.lower() in ["guitar", "g", "guitare", "guitars", "guit", "guita"]):
        instrument = "guitar"
    if(musician_instru.lower() in ["piano", "keyboards", "keyboard", "claviers", "kbds", "ke", "keys", "p", "k"]):
        instrument = "piano/clavier"
    if(musician_instru.lower() in ["trombon", "trombone"]):
        instrument = "trombon"
    if(musician_instru.lower() in ["violin", "violon", "viola", "1st violin", "2nd violin", "vln"]):
        instrument = "violin"
    if(musician_instru.lower() in ["cello", "cell"]):
        instrument = "cello"
    if(musician_instru.lower() in ["flut", "flute"]):
        instrument = "flut"
    if(musician_instru.lower() in ["dj", "sampler", "turntables", "tabl", "turntable", "laptop/ad", "laptop"]):
        instrument = "dj/laptop/sampler"

    return instrument

## TODO : must be OPTIMIZE

def create_edge_instru(dic, pds, G):
    for keyinstru in dic:
        for instru in dic[keyinstru]:
            if(instru != keyinstru):
                G.addedgeweight(keyinstru, instru, pds[keyinstru][instru])
                

# Build edges between nodes
def create_edge(dic_alb_musician, dict_pds, G, create_dic_instru = False):
    dic_instru_mus = {}
    for k in dic_alb_musician:
        for kk in dic_alb_musician:
            if(k != kk):
                for musician in dic_alb_musician[k]:
                    for musician2 in dic_alb_musician[k]:
                        if(musician != musician2):
                            if(musician != "" and musician != " " and len(musician) > 2):
                                if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                    musician_name, musician_instru = get_name_and_instru(musician)
                                    musician_name = clean_musician_name_unicode(musician_name)                    
                                    
                                    musician2_name, musician2_instru = get_name_and_instru(musician2)
                                    musician2_name = clean_musician_name_unicode(musician2_name) 
                                        
                                    if("(" not in musician_name and ")" not in musician_name and "(" not in musician2_name and ")" not in musician2_name):
                                        G.addedgeweight(musician_name, musician2_name, dict_pds[musician][musician2])
                                        
                                        if(create_dic_instru):
                                            instrument = filter_instrument(musician_instru)
                                            instrument2 = filter_instrument(musician2_instru)
                                                                
                                            # add to dico instrument
                                            if(instrument != "unknown" and instrument2 != "unknown"):
                                                if(instrument not in dic_instru_mus):
                                                    dic_instru_mus[instrument] = [instrument2]
                                                else:
                                                    dic_instru_mus[instrument].append(instrument2)
    return dic_instru_mus

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

def comput_weight_instru(dic_mus_instru, H):
    dic_pds_edge = {}
    tmp_instru = {}
    for instru in dic_mus_instru:
        tmp_instru[instru] = 0
    for instru in dic_mus_instru:
        dic_pds_edge[instru] = tmp_instru.copy()
    for instru in dic_mus_instru:
        for inst in dic_mus_instru[instru]:
            dic_pds_edge[instru][inst] += 1
                      
    return dic_pds_edge


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
