import pandas as pd
import numpy as np

data = pd.read_csv('Baseball Sim - Sheet1.csv')
data = data.set_index("Name")
data['1B'] = data['H']-data['2B']-data['3B']-data['HR']



single = data['1B']/data['PA']
double = data['2B']/data['PA']
triple = data['3B']/data['PA']
Home_Run = data['HR']/data['PA']
Walk = (data['BB']+data['HBP'])/data['PA']
Strike_Out = data['SO']/data['PA']
Hit_By_Pitch = data['HBP']/data['PA']
In_play_out = 1 - (single + double + triple + Home_Run + Walk + Strike_Out + Hit_By_Pitch)

Hitter_Outcomes = pd.DataFrame(single)
Hitter_Outcomes['double'] = double
Hitter_Outcomes['triple'] = triple
Hitter_Outcomes['Home_Run'] = Home_Run
Hitter_Outcomes['Walk'] = Walk
Hitter_Outcomes['Strike_Out'] = Strike_Out
Hitter_Outcomes['Hit_By_Pitch'] = Hit_By_Pitch
Hitter_Outcomes['In_Play_out'] = In_play_out

Hitter_Outcomes.columns = ['Single','Double', 'Triple', 'Home_Run','Walk','Strike_Out','Hit_By_Pitch','In_Play_Out']

#---Create Pitcher Outcomes---#
pdata = pd.read_csv('Baseball Sim - Sheet2.csv')
Pitcher_Outcomes = pdata.set_index("Name")
Pitcher_Outcomes = Pitcher_Outcomes.loc[:,['Single','Double','Triple','Home Run','BB','SO','InPlayOut']]

#League Averages
Single_Avg = np.mean(single)
Double_Avg = np.mean(double)
Triple_Avg = np.mean(triple)
HR_Avg = np.mean(Home_Run)
Walk_Avg = np.mean(Walk)
SO_Avg = np.mean(Strike_Out)
HBP_Avg = np.mean(Hit_By_Pitch)
In_play_out_Avg = np.mean(In_play_out)

#Create function to sim 600 PA

def sim(Hitter, Pitcher):
    Hitter_List = Hitter_Outcomes.loc[Hitter]
    Pitcher_List = Pitcher_Outcomes.loc[Pitcher]
    Single_f = ((Hitter_List.Single * Pitcher_List.Single)/Single_Avg)
    Double_f = ((Hitter_List.Double * Pitcher_List.Double)/Double_Avg)
    Triple_f = ((Hitter_List.Triple * Pitcher_List.Triple)/Triple_Avg)
    HR_f = ((Hitter_List.Home_Run * Pitcher_List['Home Run'])/HR_Avg)
    Walk_f = ((Hitter_List.Walk * Pitcher_List.BB)/Walk_Avg)
    Strike_Out_f = ((Hitter_List.Strike_Out * Pitcher_List.SO)/SO_Avg)
    In_Play_Out_f = ((Hitter_List.In_Play_Out * Pitcher_List.InPlayOut)/In_play_out_Avg)
    
    factor_sum = Single_f + Double_f + Triple_f + HR_f + Walk_f + Strike_Out_f + In_Play_Out_f
    
    Single_prob = Single_f/factor_sum
    Double_prob = Double_f/factor_sum
    Triple_prob = Triple_f/factor_sum
    Home_Run_prob = HR_f/factor_sum
    Walk_prob = Walk/factor_sum
    Strike_Out_prob = Strike_Out_f/factor_sum
    In_Play_Out_prob = In_Play_Out_f/factor_sum
    
    PA = 600
    Singles = Single_prob * PA
    Doubles = Double_prob * PA
    Triples = Triple_prob * PA
    Home_Runs = Home_Run_prob * PA
    Walks = Walk_prob * PA
    Strike_Outs = Strike_Out_prob * PA
    In_Play_Outs = In_Play_Out_prob * PA
    
    AB = PA - Walks
    Hits = Singles + Doubles + Triples + Home_Runs
    Times_Reached_Base = Hits + Walks
    BA = Hits/AB
    OBP = Times_Reached_Base/PA
    SLG = ((1*Singles + 2*Doubles + 3*Triples + 4*Home_Runs)/AB)
    OPS = OBP + SLG
    print(Hitter + " " + "vs." + " " + Pitcher)
    print('Plate Appearances: ' + str(PA))
    print('BB%: ' + str(round((Walks.loc[Hitter]/PA)*100,2)))
    print('K%: ' +str(round((Strike_Outs/PA)*100,2)))
    print('Home Runs: ' + str(int(Home_Runs)))
    print("  BA    OBP   SLG   OPS")
    print(round(BA.loc[Hitter],3),round(OBP.loc[Hitter],3),round(SLG.loc[Hitter],3),round(OPS.loc[Hitter],3),sep = '/')
    
sim('Ryan Braun','Justin Ferrell') 

