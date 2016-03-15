import numpy as np
import math
import sys
import thermotools_test as ThT
import EOS_PR_test as PR
import ln_gamma_test as lng
import pylab 
import time


def Q( MFrac ):
    Q1 = [ 0. for i in range( ThT.NComp ) ]
    for i in range(ThT.NComp):
        for j in range(ThT.NComp):
            Q1[ i ] = Q1[ i ] + MFrac[ i ] * MFrac[ j ] * ( PR.PREoS_Calc_b( i ) - PR.PREoS_Calc_a( i, ThT.T_Crit[i] ) / ThT.Rconst * ThT.T_System[ 0 ] )
    print
    return Q1

def D( Mfrac ):
    c = (1 / np.sqrt(2)) * np.log( np.sqrt(2)-1 )
    D1 = [ 0. for i in range( ThT.NComp ) ]
    for i in range(ThT.NComp):
        D1 = D1 + MFrac[ i ] * ( PR.PREoS_Calc_b( i ) - PR.PREoS_Calc_a( i, ThT.T_Crit[i] ) / ThT.Rconst * ThT.T_System[ 0 ] ) + ( lng.gibbs( MFrac ) / c * ThT.Rconst * ThT.T_System[ 0 ] )
    print
    return D1

def AM( MFrac ):
    AM1 = ( ThT.Rconst * ThT.T_System[ 0 ] ) * Q( MFrac ) * D( MFrac ) / ( 1 - D( MFrac ) )
    print
    return AM1

def BM( MFrac ):
    BM1 = Q( MFrac ) / ( 1 - D( MFrac ) )
    print
    return BM1

def DQ( MFrac ):
    DQ1 = [ 0. for i in range( ThT.NComp ) ]
    for j in range(ThT.NComp):
         DQ1 = DQ1 + MFrac[ j ] *( PR.PREoS_Calc_b( i ) - PR.PREoS_Calc_a( i, ThT.T_Crit[i] ) / ThT.Rconst * ThT.T_System[ 0 ] )
    print
    return DQ1

def DD( MFrac ):
    DD1 = [ 0. for i in range( ThT.NComp ) ]
    for i in range(ThT.NComp):
        DD1 = ( PR.PREoS_Calc_a( i, ThT.T_Crit[i] ) / ( PR.PREoS_Calc_b( i ) * ThT.Rconst * ThT.T_System[ 0 ] ) ) + lng.ln_gamma( MFrac ) / c
    print
    return DD1
    

# = = = = = = = = = # = = = = = = = = = # = = = = = = = = = # = = = = = = = = = #
Rconst = 8.314 # Gas constant [J/(gmol.K)]

ThT.ReadSet_Global_Variables()

MFrac = [ 0. for i in range( ThT.NComp ) ]
print '  the initial molar fraction before reading from the input.dat is ', MFrac
# declare a vector with MFrac values - molar fraction
MFrac[ 0 ] = 0.40; MFrac[ 1 ] = 0.20; # Vapour phase
#MFrac[ 2 ] = 0.10; MFrac[ 3 ] = 0.10; # Liquid phase

q = [ 0. for i in range( ThT.NComp ) ]
q = Q( MFrac )
print '  Q = ', q
print

d = [ 0. for i in range( ThT.NComp ) ]
d = D( MFrac )
print '  D = ', d
print

c = (1 / np.sqrt(2)) * np.log( np.sqrt(2)-1 )                    # c term from the eq. 2.26
print '  c = ', c
print

bm = q / ( 1 - d) 
am = bm * d
print '  bm = ', bm
print '  am = ', am
print

dq = [ 0. for i in range( ThT.NComp ) ]
dd = [ 0. for i in range( ThT.NComp ) ]
dq = DQ( MFrac )
dd = DD( MFrac ) 
print '  dq = ', dq
print '  dd = ', dd
print





        





        
