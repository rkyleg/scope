import os,sys

# Set Path
##if getattr(sys, 'frozen', False):
##    # frozen
##    pth = os.path.abspath(os.path.dirname(sys.executable)+'/scope')
##else:
##    # unfrozen
##    pth = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/scope')
##
##os.chdir(pth)

def run():
    sys.path.append(os.path.abspath('.'))
    from scope import scope
    scope.runui()

if __name__ == '__main__':
    run()