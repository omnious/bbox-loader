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
print("finding id time:", default_timer() - start, "s")

# We can compare bounding boxes (it uses the BBox ID internally)
assert info == listing[idx]

# We can also print it, to see the Bounding Box details
print(info)

# Moreover, we can also gather all the bounding boxes for a particular image
start = default_timer()
boxes = listing.find_bboxes_by_path(listing[0].path)
print("finding by path time:", default_timer() - start, "s")
for box in boxes:
    print(box.label, box.path)

# The BBoxList data structure has also some sorting capabilities.
# To make this example run faster, we will work with the first entries only.
l2 = BBoxList()
for i in range(100000):
    l2.append(listing[i])

# We can sort it by bounding box id using the builtin sorted function
start = default_timer()
l3 = sorted(l2)
print("sorting time Python:", default_timer() - start, "s")

# Or we can use the custom sorting methods, which run in parallel and faster.
start = default_timer()
l2.sort_by_id()
print("sorting time C++:", default_timer() - start, "s")
start = default_timer()
l2.sort_by_path()
print("sorting time C++:", default_timer() - start, "s")

# Finally, in order to get all items from a particular label, we can use the
# partition method, which will put them at the beginning of the list.  Note that
# this is implemented using a stable partition method, which means that the
# relative positions of items are kept: if you sort by path, then partition by
# ties, all examples of ties will be sorted by path, as well.
start = default_timer()
end = l2.partition("tie")
print("partition time:", default_timer() - start, "s")
print("found", end, "ties")
for i in range(end):
    print(l2[i].label, l2[i].path)
# The next element is not a tie, the order after the partition point is not
# undefined.
print(l2[end].label, l2[end].path)
