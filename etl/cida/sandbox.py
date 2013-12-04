from petl import *

# Test various joins
dict1 = [{"id": "1", "colour": "red"}, 
         {"id": "2", "colour": "blue"},
         {"id": "3", "colour": "green"},
         {"id": "4", "colour": "purple"},
         {"id": "5", "colour": "I must be included in the merge"}
        ]
        
dict2 = [{"id": "1", "name": "Fred"}, 
          {"id": "2", "name": "Joe"},
          {"id": "3", "name": "Stan"},
          {"id": "4", "name": "Arthur"},
          {"id": "4", "name": "Jack"},
          {"id": "4", "name": "Jonas"},
          {"id": "6", "name": "Please exlude me while i kiss the sky"}
         ]


d1 = fromdicts(dict1)

d2 = fromdicts(dict2)

print look(join(d2,d1,"id"))
print look(rightjoin(d2,d1,"id"))