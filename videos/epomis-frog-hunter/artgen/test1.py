from lib import *
b = rect(0,0,1920,1080,"#2B3442",0,0)
b += g(frog(), at(300,600,1.1))
b += g(frog(open_=True), at(900,600,1.0))
b += g(toad(), at(1400,600,1.0))
b += g(larva(), at(500,900,1.3))
b += g(beetle(), at(1300,950,1.4))
open('/tmp/t1.svg','w').write(svg(b))
