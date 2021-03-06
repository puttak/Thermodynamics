
#!/usr/bin/env python

import numpy as np
import math
import sys
import ThermoTools as ThT


def Activity_Models( X ):
    """ X (composition) has dimension NComp. """

    if ThT.Activity_Model[ 0 ] == 'Wilson_Model':
        GeRT, Gamma = Activity_WilsonModel( X )

    else:
        print 'Activity model', ThT.Activity_Model[ 0 ], 'is not available yet.'
        sys.exit()

    return GeRT, Gamma


def Activity_WilsonModel( X ):
    """ X (composition) has dimension NComp. 
        This function calculates the activity coeficient of each component in
             a mixture and the resulting Gibbs free energy in excess (Ge/RT).
                                                                               """
    # Creating a temporary array that will store Gamma for each component
    Gamma = [ 0. for i in range( ThT.NComp ) ]

    # Calculating the Gibbs free energy in excess (Ge/RT)
    GeRT = 0.
    for j in range( ThT.NComp ):
        sumg2 = 0.
        for i in range( ThT.NComp ):
            node1g = j * ThT.NComp + i
            sumg2 = sumg2 + X[ i ] *  ThT.Wilson_Lambda[ node1g ]
        GeRT = GeRT - X[ j ] * math.log( max( ThT.Residual, sumg2 ) )

    # Calculating the Activity Coefficient (Gamms)
    for k in range( ThT.NComp ):
        sum1 = 0.
        for i in range( ThT.NComp ):
            node1 = k * ThT.NComp + i
            sum1 = sum1 + X[ i ] * ThT.Wilson_Lambda[ node1 ]

        sum2 = 0.
        for j in range( ThT.NComp ):
            sum3 = 0.
            for i in range( ThT.NComp ):
                node3 = j * ThT.NComp + i
                sum3 = sum3 + X[ i ] * ThT.Wilson_Lambda[ node3 ]
            node2 = j * ThT.NComp + k
            sum2 = sum2 + X[ j ] * ThT.Wilson_Lambda[ node2 ] / max( ThT.Residual, sum3 )

        Gamma[ k ] = math.log( max( ThT.Residual, 1. - math.log( max( ThT.Residual, sum1 ) ) - sum2 ) )

    return GeRT, Gamma
