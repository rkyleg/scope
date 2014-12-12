import os,sys

pth = os.path.abspath(os.path.dirname(__file__)+'/../armadillo')
os.chdir(pth)
sys.path.append(os.path.abspath('.'))
import armadillo
armadillo.runui()