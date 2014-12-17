import os,sys

# Set Path
if getattr(sys, 'frozen', False):
    # frozen
    pth = os.path.abspath(os.path.dirname(sys.executable)+'/../armadillo')
else:
    # unfrozen
    pth = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../armadillo')

os.chdir(pth)
sys.path.append(os.path.abspath('.'))
import armadillo
armadillo.runui()