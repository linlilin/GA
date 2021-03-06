import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Individu:
    def __init__(self):
        self.kromosom = None;
        self.fitness = None;

    def setKromosom(self,x,y):
        """
        set kromosom dengan cara mencari biner dari solusi untuk dijadikan 8 kromosom
        """
        binx = bin(x)[2:].zfill(4)
        biny = bin(y)[2:].zfill(4)
        self.kromosom = list(binx+biny)

    def getKromosom(self):
        """
        mendapatkan nilai desimal dari kromosom yang berbentuk biner
        """
        intx = int("".join(self.kromosom[:4]),2)
        inty = int("".join(self.kromosom[4:]),2)
        return [intx,inty]

    def setFitness(self,f):
        """
        # fitness minimasi
        """
        self.fitness = 100-f

        """
        # fitness maksimasi
        self.fitness = f
        """

class Populasi:
    def __init__(self):
        self.individu = []

    def createNew(self,n):
        self.individu = [Individu() for x in xrange(n)]
        for x in self.individu:
            x.setKromosom(random.randint(0,15),random.randint(0,15))
            x.setFitness(self.fungsi(x.getKromosom()))

    def countFitness(self):
        for x in self.individu:
            x.setFitness(self.fungsi(x.getKromosom()))

    def fungsi(self,x):
        # return 3*x[0]**2-2*x[1]**2-4*x[0]+x[1]/2
        # return 7*x[0]-3*x[1]
        return x[0]+x[1]
        # return 100*(x[0]**2 - x[1])**2 + (1-x[0])**2

    def getFittest(self):
        _max = 0
        idx = 0
        for i in xrange(len(self.individu)):
            if (_max<self.individu[i].fitness):
                idx = i
                _max = self.individu[i].fitness
        return self.individu[idx]

    def getMinFit(self):
        _min = self.individu[0].fitness
        idx = 0
        for i in xrange(len(self.individu)):
            if (_min>self.individu[i].fitness):
                idx = i
                _min = self.individu[i].fitness
        return self.individu[idx]

class GA:
    def __init__(self):
        self.populasi = None
        self.mut_rate = 0.8
        self.gen = 18

    def parentselection(self):
        # menggunakan roullette wheel
        weight = 0
        for i in self.populasi.individu:
            weight += i.fitness
        toss=random.uniform(0,weight)
        ran=0
        for i in xrange(0,len(self.populasi.individu)) :
            ran+= self.populasi.individu[i].fitness
            if (toss < ran):
                return i

    def crossover(self,u,v):
        # menggunakan crossover 1 pivot menghasilkan 2 anak
        TP = random.randint(1,8)
        anak = [Individu() for x in range(2)]
        anak[0].kromosom = list(u[:TP]+v[TP:])
        anak[1].kromosom = list(v[:TP]+u[TP:])
        return anak

    def mutasi(self,ind):
        for x in range(len(ind)) :
            rnd = random.random()
            if rnd >= self.mut_rate :
                if ind[x] == '0' :
                    ind[x] = '1'
                else :
                    ind[x] = '0'
        return ind

ga = GA()
newpopulation = None
x = []
y = []
for gen in xrange(ga.gen):
    x.append([])
    y.append([])
    if (gen==0):
        populasi = Populasi()
        populasi.createNew(10)
        ga.populasi = populasi
    else:
        ga.populasi = newpopulation
        ga.populasi.countFitness()
    
    for z in ga.populasi.individu:
        x[gen].append(z.getKromosom()[0])
        y[gen].append(z.getKromosom()[1])

    newpopulation = Populasi()

    print "Generasi-",(gen+1)," : ",ga.populasi.getFittest().getKromosom()
    print "Fitness : ",ga.populasi.getFittest().fitness
    print "==========================="

    for mpool in xrange(len(ga.populasi.individu)/2):
        parent1 = ga.populasi.individu[ga.parentselection()]
        parent2 = ga.populasi.individu[ga.parentselection()]

        child = ga.crossover(parent1.kromosom,parent2.kromosom)

        for a in child:
            a.kromosom = ga.mutasi(a.kromosom)
            newpopulation.individu.append(a)

    newpopulation.individu.remove(newpopulation.getMinFit())

    elitism = ga.populasi.getFittest()
    newpopulation.individu.append(elitism)

fig = plt.figure()
ax = plt.axes(xlim=(-15, 15), ylim=(-15, 15))
line, = ax.plot([], [], 'ro')
# initialization function: plot the background of each frame
def init():
    line.set_data(x[0], y[0])
    return line,

# animation function.  This is called sequentially
xs = []
ys = []
def animate(i):
    # xs.append(x[i+1])
    # ys.append(y[i+1])
    xs = x[i+1]
    ys = y[i+1]
    line.set_data(xs, ys)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.

print "Solusi : ",ga.populasi.getFittest().getKromosom()
print "Hasil : ",ga.populasi.fungsi(ga.populasi.getFittest().getKromosom())
anim = animation.FuncAnimation(fig, animate,frames=ga.gen-1, init_func=None, interval=20, blit=False,repeat=False)

plt.show()