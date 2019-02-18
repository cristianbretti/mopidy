# There are a total of 21 simple (if, when, for) branches in _process
# All tests are run and the output is sent to process_unchanged
# Every time a branch is visited "branch Y..." is printed
# This output is searched to see what branches were/were not visited

visitedBranches = []
notVisitedBranches = []
for x in range (1,22):
    branchX = "branch %d" % (x)
    if branchX in open("process_unchanged").read():
        # print "branch %d visited!" % (x)
        visitedBranches.append(x)
    else:
        # print "branch %d NOT visited" % (x)
        notVisitedBranches.append(x)

print "Visited branches: "
print visitedBranches
print "NOT visited: "
print notVisitedBranches

# There are a total of 27 unraveled branches, does the same for these
visitedBranches = []
notVisitedBranches = []
for x in range (1,28):
    branchX = "branch %d" % (x)
    if branchX in open("process_unraveled").read():
        # print "branch %d visited!" % (x)
        visitedBranches.append(x)
    else:
        # print "branch %d NOT visited" % (x)
        notVisitedBranches.append(x)

print "UNRAVELED: Visited branches: "
print visitedBranches
print "UNRAVELED: NOT visited: "
print notVisitedBranches