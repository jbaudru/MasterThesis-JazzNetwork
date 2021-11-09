import network as n
import utility as util
import gui as ui

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
    uti = util.Utility()

    lst_data_set = "../data/dataset_album_wikipedia.csv"
    #lst_data_set = "../data/dataset_live_montreux.csv"

    print('1 - Creating datastructure')
    dic_mus_collab, dic_mus_year_collab = uti.get_dic_from_datasets(lst_data_set)
    #print('1.2 - Sorting data sets.')
    #dic_mus_collab, dic_mus_year_collab = uti.sort_dict_by_year(dic_mus_collab, dic_mus_year_collab)

    print('2 - Building nodes.')
    G.create_node(dic_mus_collab)

    #print('2.2 - Creating musicians data sets.')
    #G.create_csv_musician()

    print('3 - Building weighted edges.')
    pds = G.comput_weight(dic_mus_collab)
    dic_instru_mus = G.create_edge(dic_mus_collab, pds)

    #G.create_dynamic_edge(dic_mus_collab, G, dic_mus_year_collab)

    print("4 - Cleaning memory")
    dic_mus_collab.clear()
    pds.clear()
    #G.clear()

    print('5 - Drawing.')
    """
    H = n.Network(True)
    H.create_node(dic_instru_mus)
    pds2 = H.comput_weight_instru(dic_instru_mus)
    H.create_edge_instru(dic_instru_mus, pds2)
    interface = ui.Gui(H)
    interface.show_info(10, False, False)
    interface.show_network(True, True)
    """

    uti.create_csv_musician(G, "q1-q2_wiki", False, 50)

    interface = ui.Gui(G)
    #interface.show_network(False, False)
    #interface.show_community(False)
    #interface.show_occurence()
    #interface.show_clustering()
    #interface.show_rich_club_distrib()
    #interface.show_distrib_pk()
    #interface.show_dynamic_network(dic_mus_year_collab, False)
    interface.show_info(20, False, False)



if __name__ == '__main__':
    main()
