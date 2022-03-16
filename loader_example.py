from build.Release.bboxloader import BBoxList
from timeit import default_timer
from sys import argv, exit

if len(argv) < 2:
    print("Give a dataset.dat file as an input.")
    exit(1)

# Create an instance of the BBoxList object
listing = BBoxList()

# Load the whole listing into memory
start = default_timer()
listing.load(argv[1])
print("loading time:", default_timer() - start, "s")

# We can use it as if it were a normal native List
print("number of items:", len(listing))
info = listing[len(listing) - 1]
start = default_timer()

# It has some extra methods for finding a particular BBox
idx = listing.find_bbox_by_id(info.id)
print("finding time:", default_timer() - start, "s")

# We can compare bounding boxes (it uses the BBox ID internally)
assert info == listing[idx]

# We can also print it, to see the Bounding Box details
print(info)

l2 = BBoxList()
for i in range(10000):
    l2.append(listing[i])

start = default_timer()
l3 = sorted(l2)
print("sorting time Python:", default_timer() - start, "s")

start = default_timer()
l2.sort_by_id()
print("sorting time C++:", default_timer() - start, "s")
start = default_timer()
l2.sort_by_path()
print("sorting time C++:", default_timer() - start, "s")
for i in l2:
    print(i)
