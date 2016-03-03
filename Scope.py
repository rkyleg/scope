import os,sys

def run():
    sys.path.append(os.path.abspath('.'))
    from scope import scope

    open_file = None
    if len(sys.argv) > 1:
        open_file = sys.argv[1]
    scope.runui(open_file=open_file)

if __name__ == '__main__':
    run()