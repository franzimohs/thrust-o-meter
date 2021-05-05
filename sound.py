from aupyom import Sampler, Sound
from aupyom.util import example_audio_file

sampler = Sampler()

audio_file = example_audio_file()
s1 = Sound.from_file(audio_file)
sampler.play(s1)