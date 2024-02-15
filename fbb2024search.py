import mlbstatsapi
mlb = mlbstatsapi.Mlb()
def printBatterStats(name):
    statsConsidered = ["runs","hits","homeruns","strikeouts","avg","obp","ops","stolenbases","babip","atbatsperhomerun"]
    stats = ['season', 'career']
    groups = ['hitting', 'pitching']
    params = {'season': 2023}
    if len(mlb.get_people_id(name))>0:
        player_id = mlb.get_people_id(name)[0]
        stat_dict = mlb.get_player_stats(player_id, stats=stats, groups=groups, **params)
        season_hitting_stat = stat_dict['hitting']['season']
        for split in season_hitting_stat.splits:
            for k, v in split.stat.__dict__.items():
                if k in statsConsidered:
                    print(k, v)

def printPitcherStats(name):
    statsConsidered = ["era","runs","avg","strikeouts","gamesstarted","gamesplayed","whip","strikeoutsper9inn","strikeoutwalkratio","walksper9inn","hitsper9inn"]
    stats = ['season', 'career']
    groups = ['hitting', 'pitching']
    params = {'season': 2023}
    if len(mlb.get_people_id(name))>0:
        player_id = mlb.get_people_id(name)[0]
        stat_dict = mlb.get_player_stats(player_id, stats=stats, groups=groups, **params)
        season_hitting_stat = stat_dict['pitching']['season']
        for split in season_hitting_stat.splits:
            for k, v in split.stat.__dict__.items():
                if k in statsConsidered:
                    print(k, v)

def getPitcherStats(name):
    statsReturn = dict()
    statsConsidered = ["gamesstarted","era","avg","strikeouts","whip","runs"]
    stats = ['season', 'career']
    groups = ['hitting', 'pitching']
    params = {'season': 2023}
    if len(mlb.get_people_id(name))>0:
        player_id = mlb.get_people_id(name)[0]
        stat_dict = mlb.get_player_stats(player_id, stats=stats, groups=groups, **params)
        season_hitting_stat = stat_dict['pitching']['season']
        for split in season_hitting_stat.splits:
            for k, v in split.stat.__dict__.items():
                if k in statsConsidered:
                    statsReturn[k]=(v)
    return statsReturn

def getBatterStats(name):
    statsReturn = dict()
    statsConsidered = ["hits","homeruns","strikeouts","avg","obp","runs","babip"]
    stats = ['season', 'career']
    groups = ['hitting', 'pitching']
    params = {'season': 2023}
    if len(mlb.get_people_id(name))>0:
        player_id = mlb.get_people_id(name)[0]
        stat_dict = mlb.get_player_stats(player_id, stats=stats, groups=groups, **params)
        season_hitting_stat = stat_dict['hitting']['season']
        for split in season_hitting_stat.splits:
            for k, v in split.stat.__dict__.items():
                if k in statsConsidered:
                    statsReturn[k]=(v)
    return statsReturn
ranks = dict()
vals = dict()
plaInRank = dict()
import os
import csv
with open("FBB2024Helper.csv") as datafile:
    for line in datafile:
        line=line.strip().split(',')
        ranks[line[3]]=line[0]+", "+line[1]
        vals[line[3]]=int(line[2])
        plaInRank[line[3]] = list()
class Player:
    name = ""; rank = ""; team = "";pos ="";age=0;proj=0;estVal=0;taken=False; notes = ""
    def __init__(self,lst):
        self.name = lst[1]
        self.rank = lst[0]
        self.team = lst[2]
        self.pos = lst[3]
        self.age = int(lst[4])
        self.proj = float(lst[5])
        if len(lst)>7:
            self.notes = lst[7]
        self.estVal = vals[self.rank]
        if lst[6]=="0":
            self.taken=False
        elif lst[6]=="1":
            self.taken=True
    
    def printPlayer(self):
        term_size = os.get_terminal_size()
        print("-"*term_size.columns)
        print ("{}, {}, {}".format(self.name,self.pos,self.age))
        print("{}, Val: {}, Projected Points: {}".format(ranks[self.rank],self.estVal,self.proj))
        if "SP" in self.pos or "RP" in self.pos:
            stats = getPitcherStats(self.name)
            print("GS: {}, ERA: {}, AVG: {}, Strikeouts: {}".format(stats["gamesstarted"],stats["era"],stats["avg"],stats["strikeouts"]))
        else:
            stats=getBatterStats(self.name)
            print("H: {}, R: {}, HR: {}, K: {}, AVG: {}, OBP: {}, BABIP: {}".format(stats["hits"],stats["runs"],stats["homeruns"],stats["strikeouts"],stats["avg"],stats["obp"],stats["babip"]))
        print(self.notes)

    def __lt__(self,other):
        return self.proj < other.proj
    def __eq__(self, other):
        return self.proj == other.proj

players = dict()
with open("FBB2024.tsv") as datafile:
    for line in datafile:
        line=line.strip().split('\t')
        player = Player(line)
        plaInRank[player.rank].append(player)
        players[player.name] = player

while True:
    print("\n")
    usr = input("Player Name/Class: ").strip()
    if usr in players:
        if not players[usr].taken:
            players[usr].printPlayer()
        else:
            print("TAKEN")
    elif usr in plaInRank:
        rankList = []
        for player in plaInRank[usr]:
            if not player.taken:
                rankList.append(player)
        rankList = sorted(rankList,reverse=True)
        for player in rankList:
            player.printPlayer()
    elif usr[0:2]=="t-":
        usr = usr[2:]
        if usr in players:
            players[usr].printPlayer()
            players[usr].taken=True
    elif usr=="clear":
        for name in players:
            player = players[name]
            if player.taken:
                player.taken=False
    elif usr=="exit":
        with open("FBB2024.tsv", "w",newline='') as tsvfile:
            for name in players:
                player = players[name]
                writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
                if player.taken:
                    writer.writerow([player.rank,player.name,player.team,player.pos,player.estVal,player.proj,"1"])
                else:
                    writer.writerow([player.rank,player.name,player.team,player.pos,player.estVal,player.proj,"0"])

        break
    elif usr=="t5":
        available=[]
        for name in players:
            player = players[name]
            if not player.taken:
                available.append(player)
        available = sorted(available,reverse=True)
        for player in available[0:6]:
            player.printPlayer()
    elif usr=="t10":
        available=[]
        for name in players:
            player = players[name]
            if not player.taken:
                available.append(player)
        available = sorted(available,reverse=True)
        for player in available[0:11]:
            player.printPlayer()
    elif usr[0:2]=="s-":
        if usr[2:] in players:
            if "SP" in players[usr[2:]].pos or "RP" in players[usr[2:]].pos:
                printPitcherStats(usr[2:])
            else:
                printBatterStats(usr[2:])
    else:
        print("Invalid Input")
    
    