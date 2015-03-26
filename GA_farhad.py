import random

def fitness(f):
    return 100-(1/(f+0.1))

def fungsi(x):
    return 3*x[0]**2+2*x[1]**2-4*x[0]+x[1]/2

def encode(x,y):
    binx = bin(x)[2:].zfill(4)
    biny = bin(y)[2:].zfill(4)
    return list(binx+biny)

def decode(x):
    intx = int(x[:4],2)
    inty = int(x[4:],2)
    return [intx,inty]

def populasi(jml):
    return [encode(random.randint(0,10),random.randint(0,10)) for x in xrange(jml)]

def roulette(x):
    weight=sum(x)
    toss=random.uniform(0,weight)
    ran=0
    for i in xrange(0,len(fit)) :
        ran+=fit[i]
        if (toss < ran):
            return i

def crossover(u,v):
    TP = random.randint(1,8)
    anak = []
    anak.append(list(u[:TP]+v[TP:]))
    anak.append(list(v[:TP]+u[TP:]))
    return anak

population = []
fit = []
jmlindividu = 100
newpopulation = []
jml= 0

for gen in xrange(100):
    if (gen==0):
        population = populasi(jmlindividu)
    else:
        population = newpopulation
        newpopulation = []
    fit = [fitness(fungsi(decode("".join(x)))) for x in population]

    for mpool in xrange(jmlindividu/2):
        parent1 = population[roulette(fit)]
        parent2 = population[roulette(fit)]

        child = crossover(parent1,parent2)

        for a in child:
            newpopulation.append(a)

    jml=0
    print decode("".join(population[fit.index(max(fit))])),fit[fit.index(max(fit))]

print decode("".join(population[fit.index(max(fit))])),fit[fit.index(max(fit))]