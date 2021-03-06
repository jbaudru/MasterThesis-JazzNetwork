import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap
import community as community_louvain
import numpy as np
from decimal import Decimal
from itertools import islice

import math
import gc

import tophubstat as ths

class Gui:
    def __init__(self, graph):
        self.network = graph

    def show_info(self, num_of_node_to_prt = 10, in_q1_q2 = False, neighbors = False):
        _, deg, nb_musician = self.network.computeoccudeg()
        d = dict(self.network.getdegree())
        print('==========================================')
        print("Avg. clustering coefficient : ", nx.average_clustering(nx.Graph(self.network.getgraph())))
        #print("Clustering coefficient : ", nx.generalized_degree(nx.Graph(self.network.getgraph())))
        print("Transitivity value : ", nx.transitivity(nx.Graph(self.network.getgraph())))
        partition = community_louvain.best_partition(nx.Graph(self.network.getgraph()))
        print("Number of community : ", max(partition.values())+1)
        print("Modularity : ", community_louvain.modularity(partition, self.network.getgraph()))
        print("Total number of nodes : ", nb_musician)
        print("Average degree : ", sum(deg)/len(deg))
        print("Max. degree : ", max(deg))
        print("Min. degree : ", min(deg))
        max_value = []
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])} # Sort dict in order way
        if(in_q1_q2):
            print('==========================================')
            print("List of nodes whose degree is between the fst. quartile and the sd. quartile :")
            d_q1_q2 = dict(list(d.items())[len(d)//4:len(d)//2])
            lst_musicien = list(islice(d_q1_q2.items(), num_of_node_to_prt))
            for mus in lst_musicien:
                print(mus[0], "(deg = ", d_q1_q2[mus[0]],")")
        else:
            print('==========================================')
            print("List of most connected nodes and their degree :")
            d_top = dict(list(d.items())[-num_of_node_to_prt:])
            i = num_of_node_to_prt
            for mus in d_top:
                if(not neighbors):
                    i -= 1
                    print(str(i)+ ": "+ str(mus)+ " (deg="+ str(d_top[mus])+")")
                else:
                    print(mus, self.networketneighbours(mus)[0:9])
        print('==========================================')


    def show_network(self, make_circular = False, instru = False, country=False, year=False):
        if(make_circular):
            pos = nx.circular_layout(sorted(self.network.getgraph().nodes()))
        else:
            pos = nx.spring_layout(self.network.getgraph(), 2/math.sqrt(self.network.getorder()))
        d = dict(self.network.getdegree())
        H = nx.Graph()
        H.add_nodes_from(sorted(self.network.getgraph().nodes(data=True)))
        H.add_edges_from(self.network.getgraph().edges(data=True))
        edges = H.edges()
        if(instru):
            fig, _= plt.subplots(figsize=(4, 4),  dpi=200)
            color_lookup = {k:v for v, k in enumerate(sorted(set(H.nodes())))}
            low, *_, high = sorted(color_lookup.values())
            norm = colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20c) #magma

            weights = [H[u][v]['weight']/2000 for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1)/100 for v in d.values()], width=weights, node_color=[mapper.to_rgba(i) for i in color_lookup.values()], edge_color="grey", alpha=1, with_labels=True, font_size = 5, font_color = "#393939")
            #fig.set_facecolor('#8189A2')
        elif(country):
            fig, ax= plt.subplots(figsize=(4, 4),  dpi=200)
            color_lookup = {k:v for v, k in enumerate(sorted(set(H.nodes())))}
            low, *_, high = sorted(color_lookup.values())
            norm = colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20c) #magma

            weights = [H[u][v]['weight']/2 for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1)*15 for v in d.values()], width=weights, node_color=[mapper.to_rgba(i) for i in color_lookup.values()], edge_color="grey", alpha=1, with_labels=True, font_size = 5, font_color = "#393939")
            #nx.draw_networkx_labels(H, pos=pos, ax=ax)
            #ax.set_ylim(tuple(i*1.1 for i in ax.get_ylim()))
            #fig.set_facecolor('#8189A2')
        elif(year):
            fig, ax= plt.subplots(figsize=(4, 4),  dpi=300)
            color_lookup = {k:v for v, k in enumerate((sorted(H.nodes())))}
            low, *_, high = sorted(color_lookup.values())
            norm = colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20c) #magma
            d = dict(sorted(d.items()))
            weights = [H[u][v]['weight']/80 for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1)/40 for v in d.values()], width=weights, node_color=[mapper.to_rgba(i) for i in color_lookup.values()], edge_color="grey", alpha=1, with_labels=True, font_size = 2, font_color = "#393939")
            #nx.draw_networkx_labels(H, pos=pos, ax=ax)
            #ax.set_ylim(tuple(i*1.1 for i in ax.get_ylim()))
            #fig.set_facecolor('#8189A2')
        else:
            weights = [H[u][v]['weight']/2 for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1)/4 for v in d.values()], node_color ="#e4af7e", edge_color="#CBCBCB", width=weights, with_labels=True, font_size = 0.4, font_color = "#393939")

        plt.axis('off')
        #plt.savefig('net.png')
        plt.show()



    def show_distrib_pk(self):
        occ, deg, nb_musician = self.network.computeoccudeg()
        dict_occ_deg = {}; dict_pk = {}; dict_deg_gamma = {}
        lst_deg = []; lst_pk = []
        d = dict(self.network.getdegree())
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        # For each degree count the number of node of this degree
        for name in d:
            deg = d[name]
            if(deg > 2):
                if(deg not in dict_occ_deg):
                    dict_occ_deg[deg] = 1
                else:
                    dict_occ_deg[deg] += 1
        # For each degree k compute the value of P(k)
        for deg in dict_occ_deg:
            dict_pk[deg] = dict_occ_deg[deg] / nb_musician
            lst_deg.append(deg)
            lst_pk.append(dict_pk[deg])
        #fig = plt.figure()
        plt.plot(lst_deg, lst_pk, '.')
        plt.xlabel('k', fontsize=12)
        plt.ylabel('P(k)', fontsize=12)
        plt.gca().invert_yaxis()
        plt.show()
        # For each degree k compute the value of gamma
        for deg in dict_occ_deg:
            if(deg != 0 and deg != 1 and dict_pk[deg] != 0):
                dict_deg_gamma[deg] = math.log(Decimal(1/dict_pk[deg]),deg)
        avg_gamma = 0
        # Compute the average value of gamma for the degree present in the network
        for deg in dict_deg_gamma:
            avg_gamma += dict_deg_gamma[deg]
        avg_gamma = avg_gamma/len(dict_deg_gamma)
        print("Average value of gamma : ", avg_gamma)


    def show_rich_club_distrib(self):
        G = self.network.getgraph()
        G.remove_edges_from(nx.selfloop_edges(G))
        rc = nx.rich_club_coefficient(G, normalized=False, Q=100)
        lst_deg = []; lst_rc_coef = []
        total_rc = 0
        for deg in rc:
            lst_deg.append(deg)
            lst_rc_coef.append(rc[deg])
            total_rc += rc[deg]
        print("Average rich-club coef : ", total_rc/len(rc))
        fig = plt.figure()
        plt.plot(lst_deg, lst_rc_coef, '-', color='orange')
        fig.suptitle('Rich-club coefficient by degree', fontsize=12)
        plt.xlabel('Degree', fontsize=10)
        plt.ylabel('Rich-club coefficient', fontsize=10)
        plt.show()

    def show_num_of_mus_by_perf(self, dic_mus_collab):
        nb_mus_by_perf = 0
        lst_num_musi = []
        lst_alb_name = []
        for elem in dic_mus_collab:
            lst_num_musi.append(len(dic_mus_collab[elem]))
            lst_alb_name.append(elem)
            nb_mus_by_perf += len(dic_mus_collab[elem])
        print("Total : ", nb_mus_by_perf)
        print("Avg. num of mus. by perf : ", nb_mus_by_perf/len(dic_mus_collab))

        bargraph = ths.TopHubStat()
        bargraph.show_data("Title", "Num. musicians", lst_alb_name,  lst_num_musi)


    def show_occurence(self):
        occ, deg, nb_musician = self.network.computeoccudeg()
        fig = plt.figure()
        plt.plot(deg, occ, '.-',  color='orange')
        fig.suptitle('Degree distribution', fontsize=12)
        plt.xlabel('Degree', fontsize=10)
        plt.ylabel('Occurence', fontsize=10)
        plt.show()


    def show_clustering(self):
        H = nx.Graph(self.network.getgraph())
        gc =  H.subgraph(max(nx.connected_components(H)))
        lcc = nx.clustering(gc)
        cmap = plt.get_cmap('copper')
        norm = plt.Normalize(0, max(lcc.values()))
        node_colors = [cmap(norm(lcc[node])) for node in gc.nodes]
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 4))
        edges = H.edges()
        weights = [H[u][v]['weight']/10 for u,v in edges]
        nx.draw_kamada_kawai(gc, node_size=0.5, node_color=node_colors, with_labels=False, ax=ax1, width=weights, edge_color="#bfbfbf")
        fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax1)
        ax2.hist(lcc.values(), color="orange", bins=10)
        ax2.set_xlabel('Clustering')
        ax2.set_ylabel('Frequency')
        plt.tight_layout()
        plt.show()


    def show_community(self, simple_view = False):
        d = dict(self.network.getdegree())
        fig, ax = plt.subplots(figsize=(6, 6),  dpi=600)

        #edges = self.network.getgraph().edges()
        partition = community_louvain.best_partition(self.network.getgraph())

        pos = nx.spring_layout(self.network.getgraph(), 2/math.sqrt(self.network.getgraph().order())) #k=5/math.sqrt(self.G.order())
        cmap = cm.get_cmap("twilight_shifted", max(partition.values()) + 1)
        # color map pour les edges avec une valeur alpha
        edgemap = cmap(np.arange(cmap.N))
        edgemap[:,-1] = np.linspace(0.5, 1, cmap.N)
        edgemap = ListedColormap(edgemap)
        # Pour avoir les edges de la m??me couleur que les communaut??s
        cedges = []
        for node in self.network.getgraph().nodes():
            for edge in self.network.getgraph().edges(node):
                cedges.append(partition[edge[1]])
        if(simple_view):
            nx.draw_networkx(self.network.getgraph(), pos=pos, cmap=cmap, node_size=0.1, node_color=list(partition.values()), edge_color="grey", with_labels=False, width=0.05, arrows=False)
        else:
            nx.draw_networkx(self.network.getgraph(), pos=pos, node_size=[(v+1)/4 for v in d.values()], cmap=cmap, node_color=list(partition.values()), width=0.05, edge_color="#dbdbdb", connectionstyle=f'arc3,rad=0.2', style='solid', arrowstyle='-', with_labels=False, font_size = 0.0001, font_color = "#dbdbdb")
        ax.axis('off')
        fig.set_facecolor('#262626')
        plt.show()


    def show_pref_att(self, time, draw = False):
        lst_year = list(time.values())
        lst_year = list(dict.fromkeys(lst_year)) #remove duplicate year
        max_pa_by_year = []
        avg_pa_by_year = []
        pa_by_year = []
        count = 0
        count_node_by_year = []
        years = []
        # FOR WIKI NET
        #lst_year.remove("date")
        #lst_year.remove("year")
        lst_year = ['1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

        for j in range(0,len(lst_year)):
            if(lst_year[j].isnumeric()):
                #print("Creation network for year : ", lst_year[j])
                s = self.network.getdyngraph().time_slice(t_from= int(lst_year[j]), t_to= int(lst_year[j]))

                pref_att_curr_year = list(nx.preferential_attachment(s))
                #pref_att_curr_year = list(nx.adamic_adar_index(s))
                #pref_att_curr_year = list(nx.resource_allocation_index(s))
                #pref_att_curr_year = list(nx.jaccard_coefficient(s))

                max_pa_year = 0
                sum_pa_year = 0
                for it in range(0,len(pref_att_curr_year)):
                    if(pref_att_curr_year[it][2] > max_pa_year):
                        max_pa_year = pref_att_curr_year[it][2]
                    sum_pa_year += pref_att_curr_year[it][2]

                    pa_by_year.append(pref_att_curr_year[it][2])
                    count += 1

                if(len(pref_att_curr_year) != 0):
                    avg_pa_year = sum_pa_year/len(pref_att_curr_year)
                else:
                    avg_pa_year = 0
                #print("     Max P.A. score :", max_pa_year)
                #print("     Avg P.A. score :", avg_pa_year)

                avg_pa_by_year.append(avg_pa_year)
                max_pa_by_year.append(max_pa_year)
                count_node_by_year.append(s.number_of_nodes())
                years.append(lst_year[j])

        print(count)
        print("Avg pref att : ", sum(pa_by_year)/count)

        fig = plt.figure(figsize=(15,3), dpi=100)
        plt.plot(years, max_pa_by_year, '.-',  color='orange', label='Max. P.A. score')
        plt.ylabel('Score', fontsize=10)
        plt.xlabel('Years', fontsize=10)
        plt.xticks(rotation = 45)
        plt.xticks(fontsize=5)
        plt.legend()
        plt.show()

        fig = plt.figure(figsize=(15,3), dpi=100)
        plt.plot(years, avg_pa_by_year, '.-',  color="#918aee", label='Avg. P.A. score')
        plt.ylabel('Score', fontsize=10)
        plt.xlabel('Years', fontsize=10)
        plt.xticks(rotation = 45)
        plt.xticks(fontsize=5)
        plt.legend()
        plt.show()

        fig = plt.figure(figsize=(15,3), dpi=100)
        plt.plot(years, count_node_by_year, '.-',  color="#ee8adf", label='Number of node')
        plt.ylabel('Count', fontsize=10)
        plt.xlabel('Years', fontsize=10)
        plt.xticks(rotation = 45)
        plt.xticks(fontsize=5)
        plt.legend()
        plt.show()
