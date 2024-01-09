import ai
import game
import copy
import time
# próba odpalenia programu na GPU, chyba nie działa????? from numba import jit, cuda

# rozgrywa mecz i zwraca wynik 1. gracza


def compare(game, player1, player2):
    game1 = copy.deepcopy(game)
    game2 = copy.deepcopy(game)
    res1 = game1.match(player1, player2)
    res2 = game2.match(player2, player1)
    res = res1-res2
    del game1, game2
    return res

# to coś do odpalania na gpu
# @jit(target_backend='cuda',forceobj=True)


# ocenia generacje na podstawie turnieju każdy z każdym na losowych rozdaniach
# no_rounds - ile rozdań jest rozegranych między 2 botami
def eval_gen(no_rounds, generation):

    start = time.time()
    to_update = 5
    for agent in generation.agents:
        agent.reset_score()
    for i in range(0, int(generation.size-1)):
        for j in range(i+1, generation.size):
            for n in range(0, no_rounds):
                g = copy.deepcopy(game.Game())
                g.setrandom()
                res = compare(g, generation.agents[i], generation.agents[j])
                generation.agents[i].add_score(res)
                generation.agents[j].add_score(-res)
                if time.time()-start > to_update:
                    to_update += 5
                    k = n + j*no_rounds + generation.size*i*no_rounds
                    print('%.3f' % (k*100/(generation.size**2 * no_rounds)), "%")
    print('%.2f' % (time.time()-start))

# wybiera 2 najlepsze sieci z generacji i tworzy nową generacje z: 2 najelpszych z poprzedniej i po 49 mutacji każdego z nich


def evolve(old_gen):
    max1 = -100
    max2 = -100
    par1 = 0
    par2 = 0
    for agent in old_gen.agents:
        if agent.score > max1:
            max2 = max1
            max1 = agent.score
            par2 = par1
            par1 = agent
        elif agent.score > max2:
            max2 = agent.score
            par2 = agent
    new_agents = []
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
    new_gen = copy.deepcopy(ai.Generation(old_gen.size, new_agents))
    return new_gen


# kodzik który jest napisany na stałych i odpala algorytm uczenia sie
N = 50
gen = ai.Generation(100)
gen.load_from_file("gen19")
start = 19
print(gen.agents[0].weights)
test1 = 0
for i in range(start+1, N+1):
    print("generacja nr: %i" % i)
    gen.save_to_file("gen%i" % i)
    eval_gen(100, gen)

    if i == 1:
        test1 = copy.deepcopy(gen.get_best())
    if i == 10:
        test2 = copy.deepcopy(gen.get_best())
    gen = copy.deepcopy(evolve(gen))


test = ai.Generation(2, [test1, test2])
eval_gen(1000, test)
test.print_scores()
