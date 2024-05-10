Run 1:
whisperx
OMP_NUM_THREADS=8

139.93089531299998

Run 2:
whisperx
OMP_NUM_THREADS=8
asr_options={'beam_size': 5}

134.46543915299998

Run 3:
whisperx
OMP_NUM_THREADS=8
asr_options={'beam_size': 5}
torch.set_num_threads(8)

150.38884675900002

Run 4:
whisperx
asr_options={'beam_size': 5}, threads=8

194.286416145

Run 4:
whisperx
asr_options={'beam_size': 5}

137.09579502


Run 5:
whisperx

139.800892003


Run 1: 
threads: 2
workers: 4

1089.026057645

Run 2: 
threads: 2
workers: 2
651.1955

Run 3: 
threads: 1
workers: 1
451.8499

Run 4: 
threads: 4
workers: 1
684.67

Run 5: 
threads: 4
workers: 4

1266