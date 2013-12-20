from project_data import calcs, bilat

class project:  
    number_of_legs = 0  
  
    def sleep(self):  
        print "zzz"  
  
    def count_legs(self):  
        print "I have %s legs" % self.number_of_legs  
        print calcs
        
        print "Some of these calcs may need to be grouped in a tuple (1,3,2)"
        print bilat
  
class activity(project):  
    def bark(self):  
        print "Woof"
        