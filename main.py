from progressBar import ProgressBar
import random

import time
pb = ProgressBar(range(10), 'Description', step_str='running 0')
for num in pb():
    pb.set_step_str(f'running on {num + 1} ' + 'mrk' * random.randint(1, 5))
    time.sleep(1)

print('done')
