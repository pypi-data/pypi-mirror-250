import math
def calculate_triangle_area(a,b,c):
	sides = (a+b+c) / 2
	area = math.sqrt(sides * (sides  - a) * (sides  - b) * (sides  - c))
	return area