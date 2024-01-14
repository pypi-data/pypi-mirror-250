# sorthemes python library by christian

### EXAMPLE FUNCTUON ###

# Sort in ascending order
def sort_asc(val):
	n = len(val)
	for x in range(n):
		for y in range(0, n - x - 1):
			if val[y] > val[y + 1]:
				val[y], val[y + 1] = val[y + 1], val[y]
	return val
	
# Sort in descending order			
def sort_desc(val):
	n = len(val)
	for x in range(n):
		for y in range(0, n - x - 1):
			if val[y] < val[y + 1]:
				val[y], val[y + 1] = val[y + 1], val[y]
	return val
	
# All caps in sorted items			
def sort_caps(val):
	return [str(x).capitalize() for x in val]
	
# All lowercase items
def sort_lows(val):
	return [str(x).lower() for x in val]
	
# All uppercase items
def sort_ups(val):
  return [str(x).upper() for x in val]
