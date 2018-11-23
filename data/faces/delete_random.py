import os
from os import listdir
from os.path import isfile, join
import numpy as np

maxfiles = 100
names = ['Alexandra', 'Alvaro', 'Ana', 'AnaPaula', 'Angel', 'Antonio', 'Carlos',
         'Christian', 'Claudia', 'Dereck', 'Frizzi', 'Jenny', 'Jose', 'Kike',
         'Luis', 'Manuel', 'Mauricio', 'Puma', 'Ricardito']

for name in names:
    print('Removiendo de ',name)
    mypath = f"d:/users/cfonsecr/Documents/Forks/cf_ai/ai-challenge/data/faces/input_dir/{name}/"

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    np.random.shuffle(onlyfiles)

    n_files_to_delete = len(onlyfiles) - maxfiles

    if n_files_to_delete <= 0:
        continue

    for i in range(0,n_files_to_delete):
        os.remove(mypath + onlyfiles[i])


