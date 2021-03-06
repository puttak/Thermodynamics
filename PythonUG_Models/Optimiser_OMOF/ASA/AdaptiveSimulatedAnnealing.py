
#!/usr/bin/env python

import random
import time
import math
import sys
import numpy as np
import BenchmarkTests as BTest
import SA_IO as IO
import RandomGenerator as RanGen

#import pdb
#import pydbgr


    
###
### Summation of a list of reals
###
def ListSum( XList ):
    if ( len( XList ) == 1 ):
        return XList[ 0 ]
    else:
        return XList[ 0 ] + ListSum( XList[ 1 : ] )
    
###
### Reading Simulated Annealing cooling schedule and parameters
###

def ReadAll_SA():
    """Reading SA cooling schedule."""
    global SA_Minimum, SA_N, SA_NS, SA_NT, SA_MaxEvl, SA_EPS, SA_RT, SA_Temp, \
        SA_LowerBounds, SA_UpperBounds, SA_VM, SA_C, SA_Debugging, \
        SA_Testing, SA_Benchmarks

    SA_Cooling = []
    SA_Cooling_list = []
    
    SA_Benchmarks = []
    
    icount = 0
    ntest = 0
    SA_Testing = False


    with open( 'sa.in', 'r' ) as f:
        
        for line in f:
            if line[ 0 ] == '#':
                line.rstrip()
                SA_Cooling_list.append( line[ 2 : len( line ) - 1 ] )
                icount += 1
            elif ( line == '\n' ):
                line.rstrip()
            else:
                inner_list = []
                if ( ( len( SA_Cooling_list ) >= ( icount - 1 ) ) and ( str( SA_Cooling_list[ icount - 1 ] ) == 'Minimum' ) ):
                    inner_list = [ elt.strip() for elt in line.split(',') ]                    
                    SA_Cooling.append( to_bool( inner_list[ 0 ] ) )
                    
                elif ( ( len( SA_Cooling_list ) >= ( icount - 1 ) ) and ( str( SA_Cooling_list[ icount - 1 ] ) == 'Debugging' ) ):
                    inner_list = [ elt.strip() for elt in line.split(',') ]
                    SA_Cooling.append( to_bool( inner_list[ 0 ] ) )
                    
                elif ( ( len( SA_Cooling_list ) >= ( icount - 1 ) ) and ( str( SA_Cooling_list[ icount - 1 ] ) == 'Testing' ) ):
                    inner_list = [ elt.strip() for elt in line.split(',') ]
                    SA_Cooling.append( to_bool( inner_list[ 0 ] ) )
                    
                elif ( ( len( SA_Cooling_list ) >= ( icount - 1 ) ) and ( str( SA_Cooling_list[ icount - 1 ][0:9] ) == 'Benchmark' ) ):
                    ntest += 1
                    inner_list = [ elt.strip() for elt in line.split(',') ]
                    SA_Cooling.append( inner_list )
                    
                else:
                    inner_list = [ float(elt.strip()) for elt in line.split(',') ]
                    SA_Cooling.append( inner_list )

    f.close()

    SA_Minimum = SA_Cooling[ 0 ]           
    SA_N = num( SA_Cooling[ 1 ][0] )
    SA_NS = num( SA_Cooling[ 2 ][0] )
    SA_NT = num( SA_Cooling[ 3 ][0] )
    SA_MaxEvl = SA_Cooling[ 4 ][0]
    SA_EPS = SA_Cooling[ 5 ][0]
    SA_RT = SA_Cooling[ 6 ][0]
    SA_Temp = SA_Cooling[ 7 ][0] 

    SA_LowerBounds = SA_Cooling[ 8 ]
    SA_UpperBounds = SA_Cooling[ 9 ]
    SA_VM = SA_Cooling[ 10 ]
    SA_C = SA_Cooling[ 11 ]
    SA_Debugging = SA_Cooling[ 12 ]

    if SA_Cooling[ 13 ]:
        SA_Testing = SA_Cooling[ 13 ]

        if SA_Testing:
            if ( ntest > 1 ):
                for itest in range( ntest ):
                    jtest = len( SA_Cooling[ 13 + itest + 1 ] )
                    SA_Benchmarks.append( SA_Cooling[ 13 + itest + 1 ][ 0 : jtest ] )
            else:
                jtest = len( SA_Cooling[ 13 + ntest ] )
                SA_Benchmarks.append( SA_Cooling[ 13 + ntest ][0 : jtest ] )


    if ( SA_N != len( SA_LowerBounds ) ) or ( SA_N != len( SA_LowerBounds ) ) or \
            ( SA_N != len( SA_VM ) ) or ( SA_N != len( SA_C ) ):
               sys.exit("**** Stop !!! Dimensions do not match")


    """ Printing initialisation of the SA Algorithm """
    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( '============================================================ \n' )
    IO.f_SAOutput.write( '   Initialisation of the Simulated Annealing Algorithm: \n' )
    IO.f_SAOutput.write( '============================================================ \n' )
    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( 'Minimisation: {a:>10s}'.format( a = str( SA_Minimum ) ) + '\n' )
    IO.f_SAOutput.write( 'Dimension-Space: {a:4d}'.format( a = SA_N ) + '\n' )
    IO.f_SAOutput.write( 'Maximum Number of Function Evaluations: {a:4d}'.format( a = int( SA_MaxEvl ) ) + '\n' )
    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( 'NS: {a:3d}, NT: {b:3d}'.format( a = SA_NS, b = SA_NT ) + '\n' )
    IO.f_SAOutput.write( 'EPS: {a:.4e}'.format( a = SA_EPS ) + '\n' )
    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( 'Temperature: {a:.4f} \nParameter for temperature reduction (RT): {b:.4f}'.format( a = SA_Temp, b = SA_RT ) + '\n' )
    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( 'Lower Bounds: {a:}, Upper Bounds: {b:}'.format( a = SA_LowerBounds, b = SA_UpperBounds ) + '\n' )
    IO.f_SAOutput.write( 'VM: {a:}, C: {b:}'.format( a = SA_VM, b = SA_C ) + '\n' )

    if SA_Testing: # Printing tests
        IO.f_SAOutput.write( '\n' )
        IO.f_SAOutput.write( '------------------ Benchmark Test-Cases --------------------\n' )
        IO.f_SAOutput.write( '\n' )
        for itest in range( ntest ):
             TestName, Dimension, Minimum, Lower_Bounds, Upper_Bounds, VM, C, Solution, Optimal = ExtractingFields_BM( itest )
             IO.f_SAOutput.write( '{a:2d}. Test Case: {b:} ({c:1d} dimensions) -- {d:}'.format( a = itest + 1, b = TestName, c = Dimension, d = SA_Benchmarks[ itest ][ 2 ] ) + '\n' )
             IO.f_SAOutput.write( '{s:20} Lower Bounds: {a:}, Upper Bounds: {b:}'.format( s =' ', a = Lower_Bounds, b = Upper_Bounds ) + '\n' ) 
             IO.f_SAOutput.write( '{s:20} VM: {a:}, C: {b:}'.format( s =' ', a = VM, b = C ) + '\n' ) 
             IO.f_SAOutput.write( '{s:20} Optimal Vector-Solution: {a:}  (F_Opt: {b:})'.format( s = ' ', a = Solution, b = Optimal ) + '\n' )
             IO.f_SAOutput.write( '\n' )

        
        IO.f_SAOutput.write( '\n' )
        IO.f_SAOutput.write( '------------------ Benchmark Test-Cases --------------------\n' )
        IO.f_SAOutput.write( '\n' )
    


    


###
### Imposing constraints into field variables
###
def Envelope_Constraints( X, **kwargs ):
    """ This function ensures that variable 'X' is bounded """

    rand = []
    TryAgain = True
    IsNormalised = True

    if kwargs:
        for key in kwargs:
            if ( key == 'LBounds' ):
                LowerBounds = kwargs[ key ]
            elif ( key == 'UBounds' ):
                UpperBounds = kwargs[ key ]
            elif ( key == 'NDim' ):
                n = kwargs[ key ]
            elif ( key == 'TryC' ):
                Try = kwargs[ key ]
            elif ( key == 'IsNormalised' ):
                IsNormalised = kwargs[ key ]

    else:
         LowerBounds = SA_LowerBounds
         UpperBounds = SA_UpperBounds
         n = SA_N
    
    evaluations = 1
    
    if ( IsNormalised ): # Mole/Mass/Volume Fraction
        dim = n - 1
    else:
        dim = n

        
    while TryAgain:
           
        for i in range( dim ):
            if ( ( X[ i ] < LowerBounds[ i ]) | (X[ i ] > UpperBounds[ i ] ) ):
                rand = RanGen.RandomNumberGenerator( n, LowerBounds, UpperBounds )
                X[ i ] = LowerBounds[ i ] + ( UpperBounds[ i ] - LowerBounds[ i ] ) * \
                    rand[ i ]
                X[ i ] = min( max( LowerBounds[ i ], X[ i ] ), UpperBounds[ i ] )
                Try = True

        if ( IsNormalised ):
            
            Sum = ListSum( X[ 0 : dim ] )

            if ( Sum < 1. ):
                X[ n - 1 ] = 1. - Sum
                TryAgain = False
                if kwargs:
                    for key in kwargs:
                        if ( key == 'TryC' ):
                            return X, Try
                        else:
                            return X
                else:
                    return X
            else:
                for i in range( dim ):
                    rand = RanGen.RandomNumberGenerator( n, LowerBounds, UpperBounds )
                    if( evaluations % 3 == 0 ):
                        X[ i ] = rand[ i ]
                    elif ( evaluations % 7 == 0 ):
                        X[ i ] = min( rand[ i ], rand[ i + 1 ] ) / max( MinNum, float( i ), 1. / rand[ i + 1 ] )
                    elif ( evaluations % 11 == 0 ):
                        X[ i ] = abs( 1. - rand[ i ] / rand[ i + 1 ] )
                    else:
                        X[ i ] = rand[ i - 1 ]

                evaluations = evaluations + 1
                Try = True

        else:
            if kwargs:
                for key in kwargs:
                    if ( key == 'TryC' ):
                        return X, Try
                    else:
                        return X
            else:
                return X


###
### Converting anything to wither integer or float
###            
def num(s):
    """ Convert 'something' to either float or integer """
    try:
        return int(s)
    except ValueError:
        return float(s)

###
### Converting string to boolean
###
def to_bool(value): 
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

###
### Extrating cooling schedule parameters from the 'sa.in' file
###
def ExtractingFields_BM( itest ):
    """ Here we extract all relevant cooling schedule fields for the benchmark test case ITEST """

    
    TestName =  SA_Benchmarks[ itest ][ 0 ]

    Dimension = int( SA_Benchmarks[ itest ][ 1 ] )

    if str( SA_Benchmarks[ itest ][ 2 ] ).lower() in ( 'Minimum', 'minimum', 'MINIMUM', 'True', 'true' ):
        BM_Minimum = True

    elif str( SA_Benchmarks[ itest ][ 2 ] ).lower() in ( 'Maximum', 'maximum', 'MAXIMUM', 'False', 'false' ):
        BM_Minimum = False

    else:
        sys.exit( 'Option for Maximum or Minimum of the benchmark function not recognised' )
    
    i = 3 + Dimension
    Lower_Bounds = ( SA_Benchmarks[ itest ][ 3 : i ] )
    BM_Lower_Bounds = [ float( res ) for res in Lower_Bounds ]

    j = i + Dimension
    Upper_Bounds = ( SA_Benchmarks[ itest ][ i : j ] )
    BM_Upper_Bounds = [ float( res ) for res in Upper_Bounds ]

    k = j + Dimension
    VM = ( SA_Benchmarks[ itest ][ j : k ] )
    BM_VM = [ float( res ) for res in VM ]

    l = k + Dimension
    C = ( SA_Benchmarks[ itest ][ k : l ] )
    BM_C = [ float( res ) for res in C ]

    m = l + Dimension
    Sol = ( SA_Benchmarks[ itest ][ l : m ] )
    BM_Solution = [ float( res ) for res in Sol ]

    BM_Optimal = ( SA_Benchmarks[ itest ][ m ] )

    return TestName, Dimension, BM_Minimum, BM_Lower_Bounds, BM_Upper_Bounds, BM_VM, BM_C, BM_Solution, BM_Optimal


###
### Main SA loop
###
#def ASA_Loops( TestName, Ndim, Lower_Bounds, Upper_Bounds, VM, C, X_Try, Func ):
def ASA_Loops( TestName, X_Try, Func, **kwargs ):

    if kwargs:
        for key in kwargs:
            if ( key == 'LBounds' ):
                Lower_Bounds = kwargs[ key ]
            elif( key == 'UBounds' ):
                Upper_Bounds = kwargs[ key ]
            elif( key == 'Minimum' ):
                Minimum = kwargs[ key ]
            elif( key == 'NDim' ):
                Ndim = kwargs[ key ]
            elif( key == 'VM' ):
                VM = kwargs[ key ]
            elif( key == 'C' ):
                C =  kwargs[ key ]

    else:
        Lower_Bounds = SA_LowerBounds
        Upper_Bounds = SA_UpperBounds
        Ndim = SA_N
        VM = SA_VM
        C = SA_C
        Minimum = SA_Minimum

        
    """ For debugging """
    #pdb.set_trace()

    IO.f_SAOutput.write( '\n' )
    IO.f_SAOutput.write( 'Initialising SA Algorithm for: {a:}'.format( a = TestName ) + '\n' )


    """ Initialisation of a few parameters. """
    Try = False
    NAcc = 0; Nobds = 0; NFCNEV = 0; NEps = 4
    MaxNum = 1.e20
   
    NACP = [ 0 for i in range( Ndim ) ]
    XP = [ 0. for i in range( Ndim ) ]
    FStar = [ MaxNum for i in range ( NEps ) ] ; FStar[ 0 ] = Func
    
    FOpt = Func
    XOpt = X_Try

    Temp = SA_Temp
    Fraction = True


    if SA_Testing:
        Fraction = False
    

    kloop = 0 

    """ Beginning of the main outter loop: """
    while kloop <= SA_MaxEvl:

        NUp = 0; NRej = 0; NDown = 0; LNobds = 0


        """ Beginning of the m loop: """
        mloop = 0
        while mloop < SA_NT:


            """ Beginning of j loop: """
            jloop = 0
            while jloop < SA_NS:


                """ Beginning of the h loop: """
                hloop = 0
                while hloop < Ndim:

                    if Fraction:
                        dim = Ndim - 1
                    else:
                        dim = Ndim

                    for i in range( dim ):
                        rand = RanGen.RandomNumberGenerator( Ndim, Lower_Bounds, Upper_Bounds )

                        if ( i == hloop ):
                            XP[ i ] = X_Try[ i ] + VM[ i ] * ( 2. * rand[ i ] - 1. ) 
                        else:
                            XP[ i ] = X_Try[ i ]

                    if Fraction:
                        XP[ dim ] = 1. - ListSum( XP[ 0 : dim ] )
                        
                    Envelope_Constraints( XP, NDim = Ndim, LBounds = Lower_Bounds, UBounds = Upper_Bounds, TryC = Try, IsNormalised = Fraction )

                    if Try:
                        LNobds += 1
                        Nobds += 1

                    FuncP = BTest.TestFunction( TestName, Ndim, XP )

                    """ The function must be minimum """
                    if Minimum:
                        FuncP = -FuncP

                    NFCNEV += 1


                    """ If there were more than MAXEVL evaluations of the objective function, 
                        the SA algorithm may finish """
                    if ( NFCNEV >= SA_MaxEvl ):
                        IO.f_SAOutput.write( '\n \n    ################################################################################## \n' )
                        IO.f_SAOutput.write( '{s:20} Maximum number of evaluations of the function was reached. Either increase MAXEVL or EPS or reduce RT or NT (NFCNEV: {a:})'.format( s = ' ', a = NFCNEV ) + '\n' )
                        IO.f_SAOutput.write( '{s:20} XOpt: {a:} with FOpt: {b:}'.format( s = ' ', a = XOpt, b = FOpt ) )
                        sys.exit()


                    """ The new coordinate is accepted and the objective
                        function increases """
                    if ( FuncP >= Func ):
                        X_Try = XP
                        Func = FuncP

                        if ( SA_Debugging ):
                            IO.f_SAOutput.write( '{s:20} New vector-solution is accepted ( X: {a:}) with solution {b:.4f}'.format( s = ' ', a = X_Try, b = FuncP ) + '\n' )

                        NAcc += 1
                        NACP[ hloop ] = NACP[ hloop ] + 1
                        NUp += 1

                        """ If the new FP is larger than any other point,
                            this will be chosen as the new optimum """

                        if ( FuncP > FOpt ):
                            for i in range( Ndim ):
                                XOpt[ i ] = XP[ i ]
                            FOpt = FuncP

                    else:
                        """ However if FuncP is smaller than the others, thus the Metropolis
                            criteria (Gaussian probability density function) - or any other
                            density function that may be added latter - may be used to either
                            accept or reject this coordinate.  """
                        rand = RanGen.RandomNumberGenerator( Ndim, Lower_Bounds, Upper_Bounds )
                        Density = math.exp( ( FuncP - Func ) / max( Temp, SA_EPS ) )
                        Density_Gauss = 0.5 * ( rand[ 0 ] * rand[ Ndim - 1 ] )

                        if ( Density_Gauss < Density ):
                            X_Try = XP
                            Func = FuncP

                            if ( SA_Debugging ):
                                IO.f_SAOutput.write( '\n \n ')
                                IO.f_SAOutput.write( '{s:20} Metropolis Criteria; New vector-solution is generated ( X: {a:}) with solution {b:.4f}'.format( s = ' ', a = X_Try, b = FuncP ) + '\n' )

                            NAcc += 1
                            NACP[ hloop ] = NACP[ hloop ] + 1
                            NDown += 1

                        else:
                            NRej += 1

                    """ End of h loop """
                    hloop += 1
                    
                """ End of j loop """
                jloop += 1

            """ As half of the evaluations may be accepted, thus the VM array may be adjusted """
            for i in range( SA_N ):
                Ratio = float( NACP[ i ] ) / float( SA_NS )
                if ( Ratio > 0.6 ):
                    VM[ i ] = VM[ i ] * ( 1. + C[ i ] * ( Ratio - 0.6 ) / 0.4 )

                elif ( Ratio < 0.4 ):
                    VM[ i ] = VM[ i ] * ( 1. + C[ i ] * ( 0.41 - Ratio ) / 0.4 )

                if ( VM[ i ] > ( Upper_Bounds[ i ] - Lower_Bounds[ i ] ) ):
                    VM[ i ] =  Upper_Bounds[ i ] - Lower_Bounds[ i ]
            
            #IO.f_SAOutput.write( '{s:20} {a:3d} Points rejected. VM is adjusted to {b:}'.format( s = ' ', a = NRej, b = VM ) + '\n' )


            NACP = [ 0 for i in NACP ]
            
            """ End of m loop """
            mloop += 1

        """ Checking the stopping criteria """
        Quit = True
        FStar[ 0 ] = Func

        if ( ( FOpt - FStar[ 0 ] ) <= SA_EPS ):
            Quit = True

        for i in range( NEps ):
            if ( abs( Func - FStar[ i ] ) > SA_EPS ):
                Quit = False

        if Quit:
            X_Try = XOpt

            if Minimum:
                FOpt = - FOpt

            IO.f_SAOutput.write( '\n \n     ******** TERMINATION ALGORITHM *********** \n \n ' )

            IO.f_SAOutput.write( '{s:20} Minimum was found (FOpt = {a:}) with coordinates XOpt: {b:}'.format( s = ' ', a = FOpt, b = XOpt ) + '\n' )
            IO.f_SAOutput.write( '{s:20} Number of evaluations of the function:{a:5d}. Number of rejected points:{b:5d}'.format( s = ' ', a = NFCNEV, b = NRej ) + '\n' )

            return XOpt, FOpt

        """ If the stoppage criteria can not be reached, return to the LOOP """
        Temp = SA_RT * Temp
        for i in xrange( NEps - 1, 0, -1 ):
            FStar[ i ] = FStar[ i - 1 ]

        Func = FOpt
        X_Try = XOpt
        
            
        """ End of k loop """
        kloop += 1

    

""" =========================================================================

           Main function: Starting the Simulated Annealing Algorithm

    =========================================================================  """

def SimulatedAnnealing( Method, Task, **kwargs ):

    IO.OutPut( Task, Method )

    IO.SA_GlobalVariables()

    ntests = 0
    if( Task == 'Benchmarks' ):
        ntests = IO.CheckNumberTests()
        SA_Function, SA_Minimum, SA_N, SA_NS, SA_NT, SA_MaxEvl, SA_EPS, SA_RT, SA_Temp, \
            SA_LowerBounds, SA_UpperBounds, SA_VM, SA_C, SA_Debugging, SA_Xopt, \
            SA_Fopt = IO.ReadInCoolingSchedule( No_Tests = ntests )

    elif( Task == 'Problem' ):
        if kwargs: # For Problems
            for key in kwargs:
                if ( key == 'FileName' ): 
                    Problem_FileName = kwargs[ key ]

            #IO.ReadInCoolingSchedule( File_Name = Problem_FileName )
            rub1 = [], rub2 = []
            SA_Function, SA_Minimum, SA_N, SA_NS, SA_NT, SA_MaxEvl, SA_EPS, SA_RT, SA_Temp, \
                SA_LowerBounds, SA_UpperBounds, SA_VM, SA_C, SA_Debugging, rub1, \
                rub2 =  IO.ReadInCoolingSchedule( File_Name = Problem_FileName )
            ntests = 0

        else: 
            sys.exit( 'Option not found' )

    else:
        sys.exit( 'Option not found' )


    """ Calling main SA loop: """


    for itest in range( ntests ):

        Function = SA_Function[ itest ]
        Ndim = SA_N[ itest ]
        Minimum = SA_Minimum[ itest ]
        NS = SA_NS[ itest ]
        NT = SA_NT[ itest ]
        MaxEvl = SA_MaxEvl[ itest ]
        EPS = SA_EPS[ itest ]
        RT = SA_RT[ itest ]
        Temp = SA_Temp[ itest ]
        LowerBounds = SA_LowerBounds[ itest ]
        UpperBounds = SA_UpperBounds[ itest ]
        VM = SA_VM[ itest ]
        C = SA_C[ itest ]
        Debugging = SA_Debugging[ itest ]

        if( Task == 'Benchmarks' ):
            XSolution = SA_Xopt[ itest ]
            FSolution = SA_Fopt[ itest ]

        

        """ Initial guess-solution obtained randomly """
        X_Guess = []
        X_Guess = RanGen.RandomNumberGenerator( Ndim, LowerBounds, UpperBounds )

        """ Calling the function for the first time before the SA main loop """
        Func = BTest.TestFunction( Function, Ndim, X_Guess )
        print 'X,F:', Function, X_Guess, Func



            
        X_OPT, F_OPT = ASA_Loops( Function, Ndim, Minimum, NS, NT, MaxEvl, EPS, RT, Temp, \
                                      LowerBounds, UpperBounds, VM, C, Debugging, \
                                      X_Guess, Func )
                                
















