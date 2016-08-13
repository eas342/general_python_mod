import corner

def test_sigprint(val,sig,desired=None):
    outval = corner.sigprint(val,sig)
    if outval == desired:
        print 'Passed'
    else:
        print 'Fail:'
        print "Input: ",val,", nsig= ",sig
        print "Got: ",outval
        print "Desired: ",desired
    
def test_roundfromErr(val,err,desired=None):
    outval, outerr = corner.roundfromErr(val,err)
    if (outval == desired[0]) and (outerr == desired[1]):
        print 'Passed'
    else:
        print 'Fail:'
        print "Input: ",val," +/- ",err
        print "Got: ",outval," +/- ",outerr
        print "Desired: ",desired[0]," +/- ",desired[1]
    
if __name__ == "__main__":
    
    test_sigprint(123.44738,2,desired="120")
    test_sigprint(0,2,desired="0.0")
    test_sigprint(0.9999,2,desired="1.0")
    test_sigprint(1e5,2,desired="1.0e+05")
    test_roundfromErr(222.23,121.443,desired=["220","120"])
    test_roundfromErr(1432.3,77,desired=["1432","77"])
    test_roundfromErr(-1432.3,77,desired=["-1432","77"])
    test_roundfromErr(0,0.773422,desired=["0.00","0.77"])
    test_roundfromErr(2.5,0.3,desired=["2.50","0.30"])
    