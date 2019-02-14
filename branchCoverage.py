# There are a total of 10 simple (if/while/for) branches in next_track
# All tests are run and the output is saved in next_track_unchanged
# Every time a branch Y is entered, "... branch Y" is printed.
# This output is then searched to see which branches were/were not visited

print("total number of simple branches in next_track is 10")
for x in range (1,11):
    branchX = "branch %d" % (x)
    if branchX in open("next_track_unchanged").read():
        print "branch %d visited!" % (x)
    else: 
        print "branch %d was NOT visited!" % (x)

# Does the same, but checks the unraveled version of next_track which has 14 branches
print("total number of simple branches in next_track is 10")
for x in range (1,15):
    branchX = "branch %d" % (x)
    if branchX in open("next_track_unraveled").read():
        print "branch %d visited!" % (x)
    else: 
        print "branch %d was NOT visited!" % (x)



