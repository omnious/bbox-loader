from build.Release.bboxloader import InfosList
from timeit import default_timer
from sys import argv, exit

if len(argv) < 2:
    print("Give a dataset.dat file as an input.")
    exit(1)

listing = InfosList()
start = default_timer()
listing.load(argv[1])
print("loading time:", default_timer() - start, "s")
print("number of items:", len(listing))
info = listing[len(listing) - 1]
start = default_timer()
idx = listing.find_bbox_id(info.bbox_id)
print("finding time:", default_timer() - start, "s")
assert info == listing[idx]
print(info)
