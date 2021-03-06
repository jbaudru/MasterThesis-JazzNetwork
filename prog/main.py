import network as n
import utility as util
import gui as ui
import tophubstat as ths


def main():
    """
    uti = util.Utility()
    lst_data_set = "../data/neworleans_heritage/neworlean.csv"
    uti.csv_comma_to_semicolon(lst_data_set, "../data/dataset_neworlean.csv")
    """
    G = n.Network(False, True)
    uti = util.Utility()

    lst_data_set = "../data/dataset_album_wikipedia.csv"
    lst_data_set = "../data/dataset_live_montreux.csv"
    #lst_data_set = "../data/dataset_neworlean.csv"

    uti.eval_quality_dataset(lst_data_set)


    print('1 - Creating datastructure')
    dic_mus_collab, dic_mus_year_collab = uti.get_dic_from_datasets(lst_data_set)
    print('1.2 - Sorting data sets.')
    dic_mus_collab, dic_mus_year_collab = uti.sort_dict_by_year(dic_mus_collab, dic_mus_year_collab)

    print('2 - Building nodes.')
    G.create_node(dic_mus_collab)

    #print('2.2 - Creating musicians data sets.')
    #G.create_csv_musician()

    print('3.1 - Computing weight of edges.')
    pds = G.comput_weight(dic_mus_collab)
    print('3.2 - Building weighted edges.')
    dic_instru_mus = G.create_edge(dic_mus_collab, pds, dic_mus_year_collab)

    print('3.3 - Building dynamic edges.') # USEFUL FOR PA SCORE
    G.create_dynamic_edge(dic_mus_collab, G, dic_mus_year_collab)


    #print("4 - Cleaning memory")
    #dic_mus_collab.clear()
    #pds.clear()


    print('5 - Drawing.')

    #G.getScaleFree()

    # Pie graph, all instru Montreux
    tophubstat = ths.TopHubStat("../data/top_hub_montreux.csv")
    #print(dic_instru_mus)
    ins = {}
    for instru in dic_instru_mus:
        #print(instru)
        for inst in dic_instru_mus[instru]:
            if(inst not in ins):
                ins[inst] = 1
            else:
                ins[inst] += 1
    print(ins)
    ins = {k: v for k, v in sorted(ins.items(), key=lambda item: item[1])}
    lst_x = []; lst_y = []
    for elem in ins:
        lst_x.append(elem)
        lst_y.append(ins[elem])
    tophubstat.show_data("Instrument","Count", lst_x, lst_y)


    interface = ui.Gui(G)
    #interface.show_info(10, False, False)

    #uti.cmpt_avg_number_of_mus_by_alb(dic_mus_collab)
    #interface.show_pref_att(dic_mus_year_collab)
    #interface.show_network(False, False, False, False)

    #interface.show_clustering()
    #interface.show_distrib_pk()
    #interface.show_rich_club_distrib()
    #G.export("NET-New-Orleans")
    #interface.show_community(True)
    #interface.show_occurence()

    #TODO : Review the plot, plot bar
    #interface.show_num_of_mus_by_perf(dic_mus_collab)


    # META INSTRU
    """
    H = n.Network(True)
    H.create_node(dic_instru_mus)
    pds2 = H.comput_weight_instru(dic_instru_mus)
    #print(dic_instru_mus["Guitar"])
    #print(pds2["Guitar"])
    H.create_edge_instru(dic_instru_mus, pds2)
    H.export("META_instru_Montreux")
    interface = ui.Gui(H)
    #interface.show_info(10, False, False)
    interface.show_network(True, True, False, False)


    tophubstat = ths.TopHubStat("../data/top_hub_montreux.csv")
    dic_mus_country = tophubstat.getdictCountry()
    #print(dic_mus_country)

    # META COUNTRY
    H = n.Network(True)
    dic_country_country = uti.get_collab_country(dic_mus_country, dic_mus_collab)


    H.create_node(dic_country_country)
    pds2 = H.comput_weight_instru(dic_country_country)
    H.create_edge_instru(dic_country_country, pds2)
    H.export("META_country_Montreux")
    interface = ui.Gui(H)
    #interface.show_info(10, False, False)
    interface.show_network(True, False, True, False)


    # META YEAR
    H = n.Network(True)
    dic_year_year = uti.get_collab_year(dic_mus_collab, dic_mus_year_collab)

    dic_year_year = dict(sorted(dic_year_year.items()))

    #print(dic_year_year)
    H.create_node(dic_year_year)
    pds2 = H.comput_weight_instru(dic_year_year)
    H.create_edge_instru(dic_year_year, pds2)
    H.export("META_year_Wiki")
    interface = ui.Gui(H)
    interface.show_network(True, False, False, True)
    interface.show_info(10, False, False)
    """

    #uti.create_csv_musician(G, "top_hub_montreux", True, 100)
    #tophubstat = ths.TopHubStat("../data/top_hub_montreux.csv")
    #tophubstat = ths.TopHubStat("../data/top_hub_wiki.csv")
    #tophubstat.getdictInstru()
    #tophubstat.showInstru()
    #tophubstat.showCity()
    #tophubstat.showSex()
    #tophubstat.showYear()
    #tophubstat.showCountry()

    """
    interface = ui.Gui(G)
    interface.show_network(False, False)
    #interface.show_community(False)
    #interface.show_clustering()
    #interface.show_rich_club_distrib()
    #interface.show_distrib_pk()
    #interface.show_dynamic_network(dic_mus_year_collab, False)
    interface.show_info(20, False, False)
    """


if __name__ == '__main__':
    main()
