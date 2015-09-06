import os,sys

# Set Path
if getattr(sys, 'frozen', False):
    # frozen
    pth = os.path.abspath(os.path.dirname(sys.executable)+'/../')
else:
    # unfrozen
    pth = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../')

os.chdir(pth)
sys.path.append(os.path.abspath('.'))
from scope import scope
scope.runui()