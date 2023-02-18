import pandas as pd
import pylab as pb
import sys
import numpy as np
from scipy.stats import scoreatpercentile

non_x3d = sys.argv[1]
x3d = sys.argv[2]

non_x3d_csv = pd.read_csv(non_x3d, skiprows=2)
x3d_csv = pd.read_csv(x3d, skiprows=2)



frametimes_cpu_nonx3d = np.array([float(i.strip().strip('"').strip()) for i in non_x3d_csv['CPU frametime']])
frametimes_cpu_x3d = np.array([float(i.strip().strip('"').strip()) for i in x3d_csv['CPU frametime']])
# frametimes_gpu_x3d = np.array([float(i.strip().strip('"').strip()) for i in x3d_csv['GPU frametime']])
# frametimes_gpu_x3d = np.array([float(i.strip().strip('"').strip()) for i in x3d_csv['GPU frametime']])

pb.hist(frametimes_cpu_nonx3d, label='5800X', bins=30, alpha=0.7, normed=True)
pb.hist(frametimes_cpu_x3d, label='5800X3D', bins=30, alpha=0.7, normed=True)

average_x3d = np.average(frametimes_cpu_x3d)
perc95_x3d = scoreatpercentile(frametimes_cpu_x3d, 95)
perc99_x3d = scoreatpercentile(frametimes_cpu_x3d, 99)

average_nonx3d = np.average(frametimes_cpu_nonx3d)
perc95_nonx3d = scoreatpercentile(frametimes_cpu_nonx3d, 95)
perc99_nonx3d = scoreatpercentile(frametimes_cpu_nonx3d, 99)

pb.axvline(average_x3d, color='r',label='average_5800x3d')
pb.axvline(perc95_x3d, color='r', linestyle='--', label='95_perc_5800x3d')
pb.axvline(perc99_x3d, color='r', linestyle=':',label='99_perc_5800x3d')
pb.axvline(average_nonx3d, color='b', label='average_5800x')
pb.axvline(perc95_nonx3d, color='b', linestyle='--',label='perc_95_5800x')
pb.axvline(perc99_nonx3d, color='b', linestyle=':', label='perc_99_5800x')
pb.xlabel("CPU Frametimes, normalised histogram, milliseconds")
pb.ylabel("Amount of frames in a bin, normalised")
pb.legend()


print("5800X3D average CPU frametimes: {:0.2f}+-{:0.2f} ms, 95 percentile: {:0.2f} ms, 99 percentile: {:0.2f} ms".format(average_x3d, np.std(frametimes_cpu_x3d), perc95_x3d, perc99_x3d)) 
print()
print("5800X average CPU frametimes: {:0.2f}+-{:0.2f} ms, 95 percentile: {:0.2f} ms, 99 percentile: {:0.2f} ms".format(average_nonx3d, np.std(frametimes_cpu_nonx3d), perc95_nonx3d, perc99_nonx3d))
print()
print("5800X3D average CPU FPS: {:0.2f}+-{:0.2f} FPS, 95 percentile: {:0.2f} FPS, 99 percentile: {:0.2f} FPS".format(1000/average_x3d, np.std(1000/frametimes_cpu_x3d), 1000/perc95_x3d, 1000/perc99_x3d)) 
print()
print("5800X average CPU FPS: {:0.2f}+-{:0.2f} FPS, 95 percentile: {:0.2f} FPS, 99 percentile: {:0.2f} FPS".format(1000/average_nonx3d, np.std(1000/frametimes_cpu_nonx3d), 1000/perc95_nonx3d, 1000/perc99_nonx3d))
print()
pb.show()

