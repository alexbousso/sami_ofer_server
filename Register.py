import sys
from Subscribers import Subscribers

if len(sys.argv) < 2:
    sys.exit('Usage: {0} e-mail'.format(sys.argv[0]))

s = Subscribers()
try:
    s.add(sys.argv[1])
except Exception as e:
    sys.exit(e.message)
print 'Registration succeeded!'
