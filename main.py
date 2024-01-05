import ai,game
import copy,time
from numba import jit, cuda
def compare(game,player1,player2):
    game1=copy.deepcopy(game)
    game2=copy.deepcopy(game)
    res1=game1.match(player1,player2)
    res2=game2.match(player2,player1)
    res=res1-res2
    del game1,game2
    return res
    
#@jit(target_backend='cuda',forceobj=True)  
def eval_gen(no_rounds,generation):
    
    start=time.time()
    to_update=5
    for agent in generation.agents:
        agent.reset_score()
    for i in range(0,int(generation.size-1)):
        for j in range(i+1,generation.size):
            for n in range(0,no_rounds):
                g = copy.deepcopy(game.Game())
                g.setrandom()
                res=compare(g,generation.agents[i],generation.agents[j])
                generation.agents[i].add_score(res)
                generation.agents[j].add_score(-res)
                if time.time()-start>to_update:
                    to_update+=5
                    k = n + j*no_rounds + generation.size*i*no_rounds
                    print('%.3f'%(k*100/(generation.size**2 *no_rounds)),"%")
    generation.print_scores()
    print('%.2f'%(time.time()-start))
    
def evolve(old_gen):
    max1=-100
    max2=-100
    par1=0
    par2=0
    for agent in old_gen.agents: 
        if agent.score>max1:
            max2=max1
            max1=agent.score
            par2=par1
            par1=agent
        elif agent.score>max2:
            max2=agent.score
            par2=agent
    new_agents=[]
    new_agents.append(copy.deepcopy(par1))
    new_agents.append(copy.deepcopy(par2))
    for i in range(1, int(old_gen.size/2)):
        b = copy.deepcopy(ai.Neural_network())
        b.mutate_from(par1)
        new_agents.append(b)
    for i in range(1, int(old_gen.size/2)):
        b = copy.deepcopy(ai.Neural_network())
        b.mutate_from(par2)
        new_agents.append(b)
    new_gen = copy.deepcopy(ai.Generation(old_gen.size,new_agents))
    return new_gen
    
gen = ai.Generation(10)
eval_gen(10,gen)
gen2= evolve(gen)

print(gen.agents[0].weights)

print("gen2")
print(gen2.agents[0].weights)

