import csv

class Parser:
    def __init__(self, path):
        self.dict_alb_musician = {} # dico avec nom album et liste des musiciens
        self.dict_alb_year = {}
        self.file = open(path, "r")


    def parse_csv(self):
        for line in self.file:
            lsttmp = line.split(";")
            if(len(lsttmp) != 1): # Avoid empty data
                lstmusician = lsttmp[-1].split(",")
                # Delete useless space and linebreak in the name
                for i in range(0, len(lstmusician)):
                    if(lstmusician[i] != ''):
                        if(lstmusician[i][-1] == ' '):
                            lstmusician[i] = lstmusician[i][:-1]
                        if(lstmusician[i][0] == ' ' or lstmusician[i][0] == '"'):
                            lstmusician[i] = lstmusician[i][1:]
                        lstmusician[i] = lstmusician[i].replace('\n', '')
                        lstmusician[i] = lstmusician[i].replace('$', 's')
                [item for item in lstmusician if item != ""]
                [item for item in lstmusician if item != " "]
                [item for item in lstmusician if len(item) < 3]
                if(lstmusician[0] != ''):
                    self.dict_alb_musician[lsttmp[0]] = lstmusician
                    self.dict_alb_year[lsttmp[0]] = lsttmp[1]


    def get_dict_musician_alb(self):
        return self.dict_alb_musician

    def get_dict_year(self):
        return self.dict_alb_year
