from espn_api.football import League, BoxPlayer
from espn_api.football.box_score import BoxScore
import json
import io
import csv


l_id = 1621950432
s_id = 2021
SWID = '{C8B48DC8-3983-476C-ADCC-10F4143340CA}'
espn_s2 = 'AEC4eR0%2BKLkvslvcSdaX2mfejHYH8adqLDSgSzhYBKnN%2BcFB%2F7t2uYjRGrSoXEgPvi5QyE2kM8RGTtXK23PPJHYBDcZBgcuaeGiURP30Y%2BdsGwF8pb6Ti2JNqbtbyC50gJypUQ9%2By50e%2FEuWaui%2BFVgms2BcqYMaH4hVHQQnNf%2FqegCKRKqQgVx87FY%2FpfhrJ6z2BY4akqHbmP8O%2BilN8QlOeHKQgWYICUAUPtl1AkQh5cqltXm5vvgTJ4GYPTGvrvkq1Acxbu7zPEH%2Bi659wIaqinSTDsAi8i7jKG0azZYgWw%3D%3D'
owners_tid = {'Mitchell':1,
              'Robert':2,
              'Jacob D':3,
              'Zachariah':4,
              'Joe':5,
              'Jacob P':6,
              'Marcus':7,
              'Amanda & Daniel':8,
              'Nick':9,
              'Sam':10,
              'Clayton':11,
              'Karson':12,
              'Matt':13,
              'Cameron':14,
              1:'Mitchell',
              2:'Robert',
              3:'Jacob D',
              4:'Zachariah',
              5:'Joe',
              6:'Jacob P',
              7:'Marcus',
              8:'Amanda & Daniel',
              9:'Nick',
              10:'Sam',
              11:'Clayton',
              12:'Karson',
              13:'Matt',
              14:'Cameron',
                     }
#league team comp vars
qb=1
rb=2
wr=2
te=1
flex=1
dst=1
k=1


teamcomp= {  'QB':qb,
             'RB':rb,
             'WR':wr,
             'TE':te,
             'D/ST':dst,
             'K':k
              }


league = League(league_id=l_id,year=s_id,espn_s2=espn_s2,swid=SWID)

def sortpt(e):
    return e.points

def optlineup(team,week):
    #league team comp vars
    qb=1
    rb=2
    wr=2
    te=1
    flex=1
    dst=1
    k=1

    teamcomp= {  'QB':qb,
                 'RB':rb,
                 'WR':wr,
                 'TE':te,
                 'D/ST':dst,
                 'K':k
                  }
    owner = owners_tid[team]
    set_lineup = []
    optimal_lineup = []
    optimal_score = 0
    actual_score = 0
    bs = league.box_scores(week)
    for c,v in enumerate(bs):
        if v.home_team.team_id == team:
            roster = bs[c].home_lineup
            print("%s's Week %s Starting Lineup Was:" % (owner,week))
        elif v.away_team.team_id == team:
            roster = bs[c].away_lineup
            print("%s's Week %s Starting Lineup Was:" % (owner,week))

    for i,j in enumerate(roster):
        if not (j.slot_position == "BE" or j.slot_position == "IR"):
            actual_score += j.points
            set_lineup.append(j)

    set_lineup.sort(reverse=True,key=sortpt)

    for j in set_lineup:
       print(j.slot_position,j.name,j.points)


    print('\n%s scored %s points in Week %s' % (owner, actual_score, week))
    roster.sort(reverse=True, key=sortpt)

    for p in roster:
        if len(optimal_lineup)<8 and teamcomp[p.position]>0:
            optimal_lineup.append(p)
            teamcomp[p.position] -= 1
    #for p in optimal_lineup:
        #print(p.name, p.position, p.points)
    remaining = [i for i in set_lineup if i not in optimal_lineup] #used to select the Flex position
    for p in remaining:
        #print(p.name, p.position, p.points)
        if p.position == ("WR" or "TE" or "RB"):
            p.slot_position = "WR/TE/RB"
            optimal_lineup.append(p)
            break

    print("\n%s's Optimal Line for Week %s Up Would Have Been:\n" % (owner, week))
    for j in optimal_lineup:
        optimal_score += j.points
        print(j.position,j.name,j.points)

    pdif = optimal_score/actual_score - 1
    difference = optimal_score - actual_score
    print('\nIn Week {}\n{} actually scored {} points\n{} could have scored {} points \nOptimal Score - Actual Score = {:.2f} points\nPercent Difference: {:2.2%}\n'\
         .format(week,owner,actual_score,owner,optimal_score,difference,pdif))
    return round(optimal_score, 2), round(actual_score,2)

o=league.teams

league.pos_list(1,"RB")
