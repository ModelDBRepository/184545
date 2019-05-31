'''
SOM (putative OLM) cell model
@author: Ferguson et al. (2015) Front. Sys. Neurosci. 
'''
from brian import *

defaultclock.dt = 0.02*ms

#OLM cell parameters 
C=180 * pF 
vr=-62.2 * mV 
vpeak=6.4 * mV 
c=-69.9 * mV 
N=1
klow=2 * nS/mV 
khigh=10  * nS/mV 
a=0.0001 /ms 
d=2.6 * pA 
vt=-53.3 *mV 
b=1 * nS 

N=1   #number of cells
mean_Iapp=100 #mean Iapplied input
Ishift_raw=40  # Ishift

time=0

#cell eqns
olm_eqs = """
Iext  : amp
Ishift : amp
k=(v<vt)*klow+(v>=vt)*khigh : (siemens/volt)
du/dt = a*(b*(v-vr)-u)            : amp
dv/dt = (k*(v-vr)*(v-vt)+Ishift+Iext -u)/C : volt
"""

#define neuron group
OLM = NeuronGroup(N, model=olm_eqs, reset ="v = c; u += d" , threshold="v>=vpeak")

#set excitatory drive 
OLM.Iext = mean_Iapp*pA

#set Ishift
OLM.Ishift = Ishift_raw*pA

#set initial conditions for each neuron
OLM.v = rand(len(OLM))*0.01 -0.065

#record all spike times for the neuron group
OLM_v = StateMonitor(OLM, 'v', record=True)

#run for x seconds of simulated time
duration = 1 * second  # 0.01 * second

net =Network(OLM,OLM_v) 
net.run(duration)

####make plot of membrane potential ####
plot(OLM_v.times,OLM_v[0]/mV)
xlabel("Time (s)")
ylabel("Membrane Potential (mV)")
title('OLM cell model with %d pA input'%(mean_Iapp))
show()
