import video as vid
import utility as uti

from os import path

import networkx as nx
import dynetx as dn

import powerlaw

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap
from itertools import islice

import pandas as pd

import math
import random
from scipy.interpolate import UnivariateSpline
import numpy as np

from ethnicolr import census_ln, pred_census_ln
import csv

class Network:
    def __init__(self, isDigraph = False):
        if(isDigraph):
            self.G = nx.MultiGraph()
        else:
            self.G = nx.Graph()
        self.G_Dynamic = dn.DynGraph()
        self.node_sizes = []
        self.uti = uti.Utility()

    def clear(self):
        self.G.clear()

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

    def getdegree(self):
        return self.G.degree

    def getedges(self):
        return self.G.edges()

    def getgraph(self):
        return self.G

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


    def create_node(self, dic_alb_musician):
        dic_instru_mus = {}
        for k in dic_alb_musician:
            for musician in dic_alb_musician[k]:
                if(musician != "" and musician != " " and len(musician) > 2):
                    musician_name, musician_instru = self.uti.get_name_and_instru(musician)
                    musician_name = self.uti.clean_musician_name_unicode(musician_name)
                    if("(" not in musician_name and ")" not in musician_name):
                        self.addnode(musician_name)


    def create_edge_instru(self, dic, pds):
        for keyinstru in dic:
            for instru in dic[keyinstru]:
                if(instru != keyinstru):
                    self.addedgeweight(keyinstru, instru, pds[keyinstru][instru])

    def comput_weight_instru(self, dic_mus_instru):
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


    def create_edge(self,dic_alb_musician, dict_pds):
        dic_instru_mus = {}
        for k in dic_alb_musician:
            for musician in dic_alb_musician[k]:
                for musician2 in dic_alb_musician[k]:
                    if(musician != musician2):
                        if(musician != "" and musician != " " and len(musician) > 2):
                            if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                musician_name, musician_instru = self.uti.get_name_and_instru(musician)
                                musician_name = self.uti.clean_musician_name_unicode(musician_name)
                                musician2_name, musician2_instru = self.uti.get_name_and_instru(musician2)
                                musician2_name = self.uti.clean_musician_name_unicode(musician2_name)
                                if("(" not in musician_name and ")" not in musician_name and "(" not in musician2_name and ")" not in musician2_name):
                                    self.addedgeweight(musician_name, musician2_name, dict_pds[musician][musician2])
                                    instrument = self.uti.filter_instrument(musician_instru)
                                    instrument2 = self.uti.filter_instrument(musician2_instru)
                                    # add to dico instrument
                                    if(instrument != "unknown" and instrument2 != "unknown"):
                                        if(instrument not in dic_instru_mus):
                                            dic_instru_mus[instrument] = [instrument2]
                                        else:
                                            dic_instru_mus[instrument].append(instrument2)
        return dic_instru_mus


    def comput_weight(self, dict_alb_musician):
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


    def create_dynamic_edge(self, dic_alb_musician, G, dic_mus_year_collab):
        for k in dic_alb_musician:
            if(str(dic_mus_year_collab[k]).isnumeric()):
                time = int(dic_mus_year_collab[k])
                for musician in dic_alb_musician[k]:
                    for musician2 in dic_alb_musician[k]:
                        if(musician != musician2):
                            if(musician != "" and musician != " " and len(musician) > 2):
                                if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                    self.adddynedge(musician, musician2, time)


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


    def get_gamma_value(self):
        lst_deg = list(dict(self.G.degree()).values())
        res = powerlaw.Fit(np.array(lst_deg)+1, xmin=10)
        print("Gamma value : ", res.alpha)
        return res.alpha


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
        plt.show()
        if(draw):
            V.create_video_from_imgs(folder, "test")
