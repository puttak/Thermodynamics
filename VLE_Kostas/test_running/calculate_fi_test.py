#!/usr/bin/env python

# a function that contains the variables to calculate the ln_greek_fi

import numpy as np
import math
import sys
import thermotools_test as ThT
import calculate_EOS_PR_test as PR
import calculate_ln_gamma_test as lng
import calculate_terms_test as terms
import pdb

def CALC_FI( iphase, frac ):

    MaxNum = 1.e10 ; MinNum = 1./ MaxNum
    lnfi = [ 0. for i in range( ThT.NComp ) ]
    #print
    #print ' * TSystem, PSystem = ', ThT.T_System[0], ThT.P_System[0]
    #print ' * the terms.AM( frac ), terms.BM( frac ) = ', terms.AM( frac ), terms.BM( frac )
    #print 
    zmax , zmin = PR.Cubic_PR( ThT.T_System[0], ThT.P_System[0], terms.AM( frac ), terms.BM( frac ) )

    DD_KC = [ 0. for i in range( ThT.NComp ) ]
    DD_KC = terms.DD( frac )
    DQ_KC = [ 0. for i in range( ThT.NComp ) ]
    DQ_KC = terms.DQ( frac )
    
    # for iphase in range( ThT.NPhase ):
    for i in range( ThT.NComp )  :
       # print ' MFrac = ', frac[ i ]
        if iphase == 0:
           z = zmax
        else:
           z = zmin
      # wrong syntax  q = ( ( 1 / ( 1 - terms.D( frac ) ) * terms.DQ( frac ) - terms.Q( frac ) / ( 1 - terms.D( frac ) **2  ) * ( 1 - terms.DD( frac ) )
      # through this syntax we read all over again and again the arrays, no need to 
      # q = ( ( 1 / ( 1 - terms.D( frac ) ) * terms.DQ( frac )[i] - terms.Q( frac ) / ( 1 - terms.D( frac ) **2  ) * ( 1 - terms.DD( frac )[i] )
        q =  ( 1 / ( 1 - terms.D( frac ) ) * DQ_KC[i] - terms.Q( frac ) / ( 1 - terms.D( frac ) **2  ) * ( 1 - DD_KC[i] ) )
        d =  terms.D( frac ) * q + terms.BM( frac ) * ( 1 - DD_KC[i] )
      # For debugging
        #pdb.set_trace()
        ti = min( max (abs( z - terms.B(frac)) , MinNum), MaxNum)
        term1 = - np.log(ti) # abs is to ensure no log of -ve number
        if abs( terms.BM( frac ) - 0. ) <= MinNum: # ensuring no div by 0
            term2 = 1. / MinNum * q * ( z - 1 )
        else:
            term2 = ( 1. / terms.BM( frac ) ) * q * ( z - 1 )

        if abs( terms.AM( frac ) - 0. ) <= MinNum : # avoiding div by 0 in term3
            t31 = MinNum
        else:
            t31 = terms.AM( frac ) 
        if  abs( terms.BM( frac ) - 0. ) <= MinNum : # avoiding div by 0 in term3
            t32 = MinNum
        else:
            t32 = terms.BM( frac )

        term3 = ( 0.5 / np.sqrt(2) ) * ( ( 1./ t31 ) * d * ThT.Rconst * ThT.T_System[ 0 ] ) - ( ( 1. / t32 ) * q )

        if abs( terms.B( frac ) - 0. ) <= MinNum : # avoiding div by 0 in term4
            t41 = MinNum
        else:
            t41 = terms.AM( frac )

        if abs( ( z / t41  + 1 + np.sqrt(2) ) - 0. ) <= MinNum : # avoiding div by 0 in term4
            t42 = MinNum
        else:
            t42 = ( z / t41  + 1 + np.sqrt(2) )

        t43 = min( max ( ( z / t41  + 1 - np.sqrt(2) ) / t42, MinNum ), MaxNum ) # avoiding -ve terms in log of term4

        term4 = np.log( t43 )
        #print ' term1 = ', term1, z, frac[ i ]
        #print ' term2 = ', term2
        #print ' term3 = ', term3
        #print ' term4 = ', term4
        lnfi[ i ] = term1 + term2 + term3 * term4
        #print '    fi = ', lnfi[ i ], ' for the MFrac = ', frac[ i ] 
    
    return lnfi

'''
ThT.ReadSet_Global_Variables()
MFrac = [ 0. for i in range( ThT.NComp ) ]
print '  the initial molar fraction before reading from the input.dat is ', MFrac
# declare a vector with MFrac values - molar fraction
MFrac[ 0 ] = 0.40; MFrac[ 1 ] = 0.20; # Vapour phase
#MFrac[ 2 ] = 0.10; MFrac[ 3 ] = 0.10; # Liquid phase
iphase = 0
phi = CALC_FI( iphase, MFrac )
print 'ln_phi = ', phi 
'''
