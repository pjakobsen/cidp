from cmd import Cmd
from etl.cida import cida

class MyPrompt(Cmd):

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit

    def do_load(self, source):
        """ Load CIDA data 
            [hpds]"""
        if source == "hpds":
            cida.load_db(source)


    def do_files(self, source):
        """ Display File Information on Scraped Files 
            [source]
        """
        
        cida.list_files(source)


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')