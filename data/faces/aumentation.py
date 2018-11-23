import Augmentor

names = ['Alexandra', 'Alvaro', 'Ana', 'AnaPaula', 'Angel', 'Antonio', 'Carlos',
         'Christian', 'Claudia', 'Dereck', 'Frizzi', 'Jenny', 'Jose', 'Kike',
         'Luis', 'Manuel', 'Mauricio', 'Puma', 'Ricardito']

for name in names:
    print('Procesando: ',name)
    p = Augmentor.Pipeline(f"d:/users/cfonsecr/Documents/Forks/ai-challenge/data/faces/input_dir/{name}/")
    p.rotate(probability=0.7, max_left_rotation=15, max_right_rotation=15)
    p.sample(100)
    p.process()






