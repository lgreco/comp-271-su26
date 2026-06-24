from Station import Station
from Trainline import Trainline

how = Station("Howard")
jar = Station("Jarvis")
mor = Station("Morse")
loy = Station("Loyola")
gra = Station("Granville")

red_line_sb = Trainline()

red_line_sb.add(how)
red_line_sb.add(jar)
red_line_sb.add(mor)
red_line_sb.add(loy)
red_line_sb.add(gra)

print(red_line_sb.contains("Granville"))  # expect True
print(red_line_sb.contains("DuPont Circle"))  # expect False
