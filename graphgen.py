from turtle import color
import matplotlib.pyplot as mp
import pandas as pd
#Function to generalize and count success rate for each ghost level
def get_data(ds):
    x = ds.iloc[:,1].values
    number_of_ghost = list(x)[1:]

    x = ds.iloc[:,4].values
    win_loss=list(x)[1:]

    number_of_ghost_set=list(set(number_of_ghost))
    number_of_ghost_set.sort()
    win_loss_count=[0]*len(number_of_ghost_set)
    for i in range(len(number_of_ghost)):
        if win_loss[i]=="success":
            win_loss_count[number_of_ghost_set.index(number_of_ghost[i])]+=1
    s=0
    for i in win_loss_count:
        s=s+i
    print(s)
    return number_of_ghost_set,win_loss_count




ds = pd.read_excel("agent1log.xlsx")
number_of_ghost_set,win_loss_count=get_data(ds)
mp.plot(number_of_ghost_set,win_loss_count,color="green")

ds = pd.read_excel("agent2log.xlsx")
number_of_ghost_set,win_loss_count=get_data(ds)
mp.plot(number_of_ghost_set,win_loss_count,color="blue")

ds = pd.read_excel("agent3log.xlsx")
number_of_ghost_set,win_loss_count=get_data(ds)
for j in range(len(win_loss_count)):
    win_loss_count[j]=win_loss_count[j]*5
mp.plot(number_of_ghost_set,win_loss_count,color="yellow")

ds = pd.read_excel("agent4log.xlsx")
number_of_ghost_set,win_loss_count=get_data(ds)
mp.plot(number_of_ghost_set,win_loss_count,color="red")

# ds = pd.read_excel("agent4wallGGlog.xlsx")
# number_of_ghost_set,win_loss_count=get_data(ds)
# mp.plot(number_of_ghost_set,win_loss_count,color="blue")

# ds = pd.read_excel("agent5log.xlsx")
# number_of_ghost_set,win_loss_count=get_data(ds)
# mp.plot(number_of_ghost_set,win_loss_count,color="blue")

mp.ylim(0,50)
mp.xlabel('Number of ghosts')
mp.ylabel('Success out of 50')
mp.title('Agent 1-4 Success rate graph \n')
mp.show()