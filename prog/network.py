import video as vid

from os import path

import networkx as nx
import dynetx as dn

import powerlaw

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap
from itertools import islice

import community as community_louvain
import pandas as pd

import math
import random
from scipy.interpolate import UnivariateSpline
import numpy as np
from decimal import Decimal

from ethnicolr import census_ln, pred_census_ln
import gender_guesser.detector as gender
import csv

class Network:
    def __init__(self, isDigraph = False):
        if(isDigraph):
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        self.G_Dynamic = dn.DynGraph()
        self.node_sizes = []
        self.GenderD = gender.Detector()
        self.isDig = isDigraph


    def addnode(self, name):
        self.G.add_node(name)
        self.G_Dynamic.add_node(name)


    def addedge(self, src, dest):
        self.G.add_edge(src, dest)


    def adddynedge(self, src, dest, time):
        if(str(time).isnumeric()): # Avoid case where there is no year in data set
            self.G_Dynamic.add_interaction(src, dest, t=time)


    def addedgeweight(self, src, dest, wt):
        self.G.add_edge(src, dest, weight=wt)

    def getnodes(self):
        return self.G.nodes

    def getneighbours(self, node):
        lst = [n for n in self.G.neighbors(node)]
        return lst

    def computeoccudeg(self):
        occurence = {}
        d = dict(self.G.degree)
        nb_musician = 0
        for key in d:
            nb_musician += 1
            if(d[key] not in occurence):
                occurence[d[key]] = 1
            else:
                occurence[d[key]] += 1
        deg = []
        occ = []
        for i in sorted(occurence.keys()):
            deg.append(i)
            occ.append(occurence[i])
        return occ, deg, nb_musician


    # Guess the sex of the musician and build a color map
    def get_sex(self):
        color_map = []
        for musician in self.getnodes():
            mus_tmp = musician.split(" ")
            gend = self.GenderD.get_gender(mus_tmp[0])

            if(gend=='male'):
                color_map.append('#DD5D41')
            elif(gend == 'mostly_male'):
                color_map.append('#CC8156')
            elif(gend=='female'):
                color_map.append('#99EB93')
            elif(gend == 'mostly_female'):
                color_map.append('#AAC87F')
            else:
                color_map.append('grey')
        return color_map

    ## TODO : move to utility class

    # Create a database with all the informations on a musician
    def create_csv_musician(self):
        dict_alb_musician = dict(self.G.degree)
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

    ## TODO : move to 'gui'

    def printInfoDyna(self, time):
        lst_year = list(time.values())
        lst_year = list(dict.fromkeys(lst_year)) #remove duplicate year

        occ, deg, nb_musician = self.computeoccudeg()
        d = dict(self.G.degree)
        print("Density all time : ", dn.density(self.G_Dynamic))

        # AUTRES PARAMETRES

    ## TODO : move to 'gui'

    def printInfo(self, num_of_node_to_prt = 10, in_q1_q2 = False, neighbors = False):
        occ, deg, nb_musician = self.computeoccudeg()
        d = dict(self.G.degree)
        print("Clustering coefficient : ", nx.average_clustering(self.G))
        print("Transitivity value : ", nx.transitivity(self.G))
        if(not self.isDig):
            partition = community_louvain.best_partition(self.G)
            print("Number of community : ", max(partition.values())+1)
        print("Total number of nodes : ", nb_musician)
        print("Average degree : ", sum(deg)/len(deg))

        max_key = []
        max_value = []

        # Sort dict in order way
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        if(in_q1_q2):
            print('==========================================')
            print("List of nodes whose degree is between the fst. quartile and the sd. quartile :")
            #Get the n musician between q1 and q2
            d_q1_q2 = dict(list(d.items())[len(d)//4:len(d)//2])
            # Take 50 of the q1-q2
            lst_musicien = list(islice(d_q1_q2.items(), num_of_node_to_prt))
            for mus in lst_musicien:
                print(mus[0], " : ", d_q1_q2[mus[0]])
        else:
            print('==========================================')
            print("List of most connected nodes and their degree :")
            d_top = dict(list(d.items())[-num_of_node_to_prt:])
            for mus in d_top:
                if(not neighbors):
                    print(mus, " : ", d_top[mus])
                else:
                    print(mus, self.getneighbours(mus)[0:9])


    # https://stackoverflow.com/questions/38408224/how-to-calculate-ebk-of-networks-with-python
    def get_gamma_value(self):
        lst_deg = list(dict(self.G.degree()).values())
        res = powerlaw.Fit(np.array(lst_deg)+1, xmin=10)
        print("Gamma value : ", res.alpha)
        return res.alpha

    ## TODO : move to 'gui'

    # RESULTAT ETRANGE -> A REVOIR
    def show_distrib_pk(self):
        occ, deg, nb_musician = self.computeoccudeg()
        dict_occ_deg = {}
        dict_pk = {}
        dict_deg_gamma = {}
        lst_deg = []
        lst_pk = []
        d = dict(self.G.degree)
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

        fig = plt.figure()
        plt.plot(lst_deg, lst_pk, '.')
        plt.xlabel('k', fontsize=12)
        plt.ylabel('P(k)', fontsize=12)
        plt.gca().invert_yaxis()
        fig.savefig('distrib_pk.png')
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

    ## TODO : move to 'gui'

    def show_rich_club_distrib(self):
        rc = nx.rich_club_coefficient(self.G, normalized=True, Q=100)
        lst_deg = []
        lst_rc_coef = []
        total_rc = 0
        for deg in rc:
            lst_deg.append(deg)
            lst_rc_coef.append(rc[deg])
            total_rc += rc[deg]

        print("Average rich-club coef : ", total_rc/len(rc))

        fig = plt.figure()
        plt.plot(lst_deg, lst_rc_coef, 'o-')
        fig.suptitle('Rich-club coefficient by degree', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Rich-club coefficient', fontsize=12)
        plt.show()

    ## TODO : move to 'gui'

    def show_occurence(self):
        occ, deg, nb_musician = self.computeoccudeg()
        fig = plt.figure()
        plt.plot(deg, occ, 'o-')
        fig.suptitle('Number of node by degree', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Occurence', fontsize=12)
        fig.savefig('occurence.png')
        plt.show()


    ## TODO : move to 'gui'
    # Function from https://stackoverflow.com/questions/64485434/how-to-plot-the-distribution-of-a-graphs-clustering-coefficient
    def show_clustering(self):
        gc = self.G.subgraph(max(nx.connected_components(self.G)))
        lcc = nx.clustering(gc)
        cmap = plt.get_cmap('autumn')
        norm = plt.Normalize(0, max(lcc.values()))
        node_colors = [cmap(norm(lcc[node])) for node in gc.nodes]
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 4))
        nx.draw_spring(gc, node_size=5, node_color=node_colors, with_labels=False, ax=ax1, edge_color="#bfbfbf")
        fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax1)
        ax2.hist(lcc.values(), bins=10)
        ax2.set_xlabel('Clustering')
        ax2.set_ylabel('Frequency')

        plt.tight_layout()
        plt.show()

    ## TODO : move to 'gui'
    # TODO : General, dessiner uniquement un seul des deux liens, éviter les doublons !
    def show_community(self, simple_view = False):
        G_mul = nx.MultiDiGraph()
        G_mul = self.G.to_directed()
        d = dict(self.G.degree)
        fig, ax = plt.subplots(figsize=(10, 6),  dpi=600)
        edges = self.G.edges()
        weights = [math.sqrt(self.G[u][v]['weight'])/4 for u,v in edges]
        partition = community_louvain.best_partition(self.G)

        pos = nx.spring_layout(self.G, 2/math.sqrt(self.G.order())) #k=5/math.sqrt(self.G.order())
        #twilight_shifted
        cmap = cm.get_cmap("twilight_shifted", max(partition.values()) + 1)

        # color map pour les edges avec une valeur alpha
        edgemap = cmap(np.arange(cmap.N))
        edgemap[:,-1] = np.linspace(0.5, 1, cmap.N)
        edgemap = ListedColormap(edgemap)

        # Pour avoir les edges de la même couleur que les communautés
        cedges = []
        for node in self.G.nodes():
            for edge in self.G.edges(node):
                cedges.append(partition[edge[1]])

        if(simple_view):
            nx.draw_networkx(G_mul, pos=pos, cmap=cmap, node_size=0.1, node_color=list(partition.values()), edge_color="#EEEEEE", with_labels=False, width=0.1, arrows=False)
        else:
            #nx.draw_networkx_nodes(G_mul, pos=pos, node_size=[v * 5 for v in d.values()], cmap=cmap, node_color=list(partition.values()), linewidths=0)
            #nx.draw_networkx_edges(G_mul, pos=pos, edge_cmap=cmap, edge_color=cedges, width=weights, connectionstyle=f'arc3,rad=0.2', arrowstyle='-', alpha=0.5, arrowsize = 0.1, min_target_margin=0)
            #nx.draw_networkx_labels(G_mul, pos=pos, font_size=2.5, font_color='white')

            #Idem que les trois ligne au dessus mais sans les edges en trans et sans bug de edges
            nx.draw_networkx(G_mul, pos=pos, node_size=[v * 0.01 for v in d.values()], cmap=cmap, node_color=list(partition.values()) , edge_cmap=edgemap, edge_color=cedges, width=weights, connectionstyle=f'arc3,rad=0.2', style='solid', arrowstyle='-', with_labels=False, font_size = 0.5, font_color = "white")
            # linewidths=0.2, edgecolors='black'

        ax.axis('off')
        fig.set_facecolor('black')
        #plt.savefig("community.png")
        plt.show()

    ## TODO : move to 'video'
    def show_dynamic_network(self, time, draw = False):
        V = vid.Video()
        folder = "../data/tmp_vid/"

        pos = nx.kamada_kawai_layout(self.G_Dynamic)
        lst_year = list(time.values())
        lst_year = list(dict.fromkeys(lst_year)) #remove duplicate year
        start = lst_year[0]

        lst_nodes = self.G_Dynamic.nodes() #get all node (a modifier si marche pas)
        final_lst_deg = dict(self.G.degree)
        lst_deg = {}

        pa_all_time = list(nx.preferential_attachment(self.G_Dynamic))
        max_pa = 0
        max_txt = ""
        for it in range(0, len(pa_all_time)):
            if(pa_all_time[it][2] > max_pa):
                max_pa = pa_all_time[it][2]
                max_txt = pa_all_time[it]
        print(max_txt)

        max_pa_by_year = []
        years = []

        for j in range(0,len(lst_year)-1):
            if(lst_year[j] != "year"):
                plt.figure(figsize=(15,10), dpi=100)
                print("Creation network for year : ", lst_year[j])

                s = self.G_Dynamic.time_slice(t_from= int(start), t_to= int(lst_year[j]))
                lst_nodes = self.G_Dynamic.nodes(t=int(lst_year[j]))

                cur_dict_deg = dn.degree(self.G_Dynamic, lst_nodes, t=int(lst_year[j]))

                lst_nodes_s = s.nodes()
                cur_dict_deg_s = dn.degree(s)


                pref_att_curr_year = list(nx.preferential_attachment(s))
                max_pa_year = 0
                for it in range(0,len(pref_att_curr_year)):
                    if(pref_att_curr_year[it][2] > max_pa_year):
                        max_pa_year = pref_att_curr_year[it][2]
                print("P.A. score max by year", max_pa_year)
                max_pa_by_year.append(max_pa_year)
                years.append(lst_year[j])

                if(draw):
                    ax = plt.gca()
                    ax.margins(0.1, 0.1)
                    ax.set_title(lst_year[j])
                    nx.draw(s, pos, node_size=[v * 2 for v in cur_dict_deg_s.values()], node_color ="#5792ad", edge_color="#bfbfbf", with_labels = True, font_size = 3, font_color = "#212121", ax=ax)
                    _ = ax.axis('off')
                    name = str(lst_year[j])+".png"
                    plt.savefig(folder + name, dpi=100)
                    #plt.show()

        fig = plt.figure()
        plt.plot(max_pa_by_year, years, 'o-')
        fig.suptitle('P.A. max score by year', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Year', fontsize=8)
        fig.savefig('max_pa_score_by_year.png')
        plt.show()
        if(draw):
            V.create_video_from_imgs(folder, "test")


    ## TODO : move to 'gui'
    def show_network(self, make_circular = False, instru = False):
        if(make_circular):
            pos = nx.circular_layout(self.G)
        else:
            pos = nx.spring_layout(self.G, 2/math.sqrt(self.G.order()))

        if(instru):
            
            edges = self.G.edges()
            weights = [self.G[u][v]['weight']/100 for u,v in edges]
            nx.draw_networkx_nodes(self.G, pos, node_size=[v * 0.5 for v in d.values()],  alpha=0.8, node_color ="#FF5733")
            nx.draw_networkx_edges(self.G, pos,  width=weights, connectionstyle=f'arc3,rad=0.2', arrowstyle='-', arrowsize = 0.1, alpha=0.1, edge_color="#212121")
            nx.draw_networkx_labels(self.G, pos, font_size = 2, font_color = "#212121")
        else:
            d = dict(self.G.degree)
            edges = self.G.edges()
            weights = [self.G[u][v]['weight']/100 for u,v in edges]
            nx.draw_networkx_nodes(self.G, pos, node_size=[v * 0.5 for v in d.values()],  alpha=0.8, node_color ="#FF5733")
            nx.draw_networkx_edges(self.G, pos,  width=weights, connectionstyle=f'arc3,rad=0.2', arrowstyle='-', arrowsize = 0.1, alpha=0.1, edge_color="#212121")
            nx.draw_networkx_labels(self.G, pos, font_size = 2, font_color = "#212121")
        plt.axis('off')
        plt.savefig("simple_network.png")
        plt.show()
