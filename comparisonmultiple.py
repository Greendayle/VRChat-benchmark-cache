import pandas as pd
import pylab as pb
import sys
import numpy as np
from scipy.stats import scoreatpercentile
import os

stuff = sys.argv[1:-1]
name = sys.argv[-1]
if len(stuff) % 2 != 0:
    raise Exception("inputs should be: csv_pathh csv2_path label1 label2...")

paths = stuff[:int(len(stuff)/2)]
labels = stuff[int(len(stuff)/2):]

datas = []
for i in paths:
    datas.append(pd.read_csv(i, skiprows=2))


frametimes_cpu = []
cmap = pb.get_cmap("tab10").colors
fig = pb.figure(figsize=(10,10))
for nr, data in enumerate(datas):
     f = np.array([float(i.strip().strip('"').strip()) for i in data['CPU frametime']])
     frametimes_cpu.append(f)
     pb.hist(f, label=labels[nr], bins=30, alpha=0.7, normed=True)
     avg = np.average(f)
     perc95 = scoreatpercentile(f, 95)
     perc99 = scoreatpercentile(f, 99)
     pb.axvline(avg, color=cmap[nr],label='average_{}'.format(labels[nr]))
     pb.axvline(perc95, color=cmap[nr], linestyle='--', label='95_perc_{}'.format(labels[nr]))
     pb.axvline(perc99, color=cmap[nr], linestyle=':',label='99_perc_{}'.format(labels[nr]))
     print("{} average CPU frametimes: {:0.2f}+-{:0.2f} ms, 95 percentile: {:0.2f} ms, 99 percentile: {:0.2f} ms".format(labels[nr], avg, np.std(f), perc95, perc99)) 
     print()

     print("{} average CPU FPS: {:0.2f}+-{:0.2f} FPS, 95 percentile: {:0.2f} FPS, 99 percentile: {:0.2f} FPS".format(labels[nr], 1000/avg, np.std(1000/f), 1000/perc95, 1000/perc99))
     print()


pb.xlabel("CPU Frametimes, normalised histogram, milliseconds")
pb.ylabel("Amount of frames in a bin, normalised")
pb.legend()
pb.title(name)
fig.tight_layout()

pb.savefig(os.path.join('img', name+'_histogram.png'))

fig, ax = pb.subplots(figsize=(10,10))
df = pd.DataFrame(data=[i.mean() for i in frametimes_cpu], index=labels, columns=['CPU Frametime, ms',])
df.plot.bar(y='CPU Frametime, ms', ax=ax)
ax.set_title(name)
ax.set_ylabel("Average CPU frametime, ms")

fig.tight_layout()
pb.savefig(os.path.join('img', name+'_barplot.png'))

df = pd.DataFrame(data=[i.mean() for i in frametimes_cpu], index=labels, columns=[name,])
df.to_csv('img/summary_cpu_frametime_ms_{}.csv'.format(name))


#~ import IPython
#~ IPython.embed()

fig, ax = pb.subplots(figsize=(10,10))

pb.boxplot(frametimes_cpu, labels=labels)
#~ maxlen = max([len(i) for i in frametimes_cpu])
#~ df = pd.DataFrame(data=np.array([np.pad(i, maxlen, mode='empty') for i in frametimes_cpu]).T, columns=labels)
#~ IPython.embed()
#~ fig, ax = pb.subplots(figsize=(10,10))
#~ df.plot.boxplot(ax=ax)
ax.set_title(name)
ax.set_ylabel("Average CPU frametime, ms")
fig.tight_layout()

pb.savefig(os.path.join('img', name+'_boxplot.png'))




pb.show()


# example:
# python .\comparisonmultiple.py .\5800x_index\just_b_club_3_spawn_people.csv .\5800x3d_vive_pro_matching_res_index\just_b_club3_spawn_people.csv .\additional_new_bench\Frametimes#Just_B_Public_A.csv .\additional_new_bench\Frametimes#Just_B_Public_B.csv 5800x 5800x3d 5800x_2 5800x3d_2 just_b_club
