
#  Python Standard Libraries
import math

#  Terminus Astro Libraries
#import tmns.astro.time.utilities as utils

class Scale:
    DELTA = 'delta'
    TAI   = 'tai'
    UT1   = 'ut1'
    UTC   = 'utc'

    @staticmethod
    def from_string( tp : str ):

        tp = str(tp).lower()
        if tp == Scale.DELTA:
            return Scale.DELTA
        if tp == Scale.TAI:
            return Scale.TAI
        if tp == Scale.UT1:
            return Scale.UT1
        if tp == Scale.UTC:
            return Scale.UTC
        return None

class Base:
    def __init__(self, data ):
        self.data = data

class TAI(Base):
    def __init__(self, data ):
        super().__init__(data)

    @staticmethod
    def from_utc( fmt ) -> TAI:
        '''
        Taken from SOFA, utctai.c, method: iauUtctai()

        Time scale transformation:  Coordinated Universal Time, UTC, to
        International Atomic Time, TAI.

        This function is part of the International Astronomical Union's
        SOFA (Standards of Fundamental Astronomy) software collection.

        Status:  canonical.

        Returned (function value):
                int      status: +1 = dubious year (Note 3)
                                  0 = OK
                                 -1 = unacceptable date

        Notes:

          2) JD cannot unambiguously represent UTC during a leap second unless
             special measures are taken.  The convention in the present
             function is that the JD day represents UTC days whether the
             length is 86399, 86400 or 86401 SI seconds.  In the 1960-1972 era
             there were smaller jumps (in either direction) each time the
             linear UTC(TAI) expression was changed, and these "mini-leaps"
             are also included in the SOFA convention.

          3) The warning status "dubious year" flags UTCs that predate the
             introduction of the time scale or that are too far in the future
             to be trusted.  See iauDat for further details.

          4) The function iauDtf2d converts from calendar date and time of day
             into 2-part Julian Date, and in the case of UTC implements the
             leap-second-ambiguity convention described above.

          Called:
             iauJd2cal    JD to Gregorian calendar
             iauDat       delta(AT) = TAI-UTC
             iauCal2jd    Gregorian calendar to JD

         References:

            McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
            IERS Technical Note No. 32, BKG (2004)

            Explanatory Supplement to the Astronomical Almanac,
            P. Kenneth Seidelmann (ed), University Science Books (1992)
        '''

        #  Get the JD value
        utc1 = fmt.as_jd()[0]
        utc2 = fmt.as_jd()[1]

        #  Put the two parts of the UTC into big-first order.
        utc_sum = math.fabs(utc1) >= math.fabs(utc2)
        if utc_sum:
            u1 = utc1
            u2 = utc2
        else:
            u1 = utc2
            u2 = utc1

        #  Get TAI-UTC at 0h today.
        #dtime = utils.jd_to_datetime( u1, u2 )
        #if dtime is None:
        #    raise Exception( f'Invalid Julian Date. {u1}, {u2}' )

#        j = iauDat(iy, im, id, 0.0, &dat0);
#   if ( j < 0 ) return j;
#
#    #  Get TAI-UTC at 12h today (to detect drift).
#   j = iauDat(iy, im, id, 0.5, &dat12)
#   if ( j < 0 ) return j;
#
#/* Get TAI-UTC at 0h tomorrow (to detect jumps). */
#   j = iauJd2cal(u1+1.5, u2-fd, &iyt, &imt, &idt, &w);
#   if ( j ) return j;
#   j = iauDat(iyt, imt, idt, 0.0, &dat24);
#   if ( j < 0 ) return j;
#
#/* Separate TAI-UTC change into per-day (DLOD) and any jump (DLEAP). */
#   dlod = 2.0 * (dat12 - dat0);
#   dleap = dat24 - (dat0 + dlod);
#
#/* Remove any scaling applied to spread leap into preceding day. */
#   fd *= (DAYSEC+dleap)/DAYSEC;
#
#/* Scale from (pre-1972) UTC seconds to SI seconds. */
#   fd *= (DAYSEC+dlod)/DAYSEC;
#
#/* Today's calendar date to 2-part JD. */
#   if ( iauCal2jd(iy, im, id, &z1, &z2) ) return -1;
#
#/* Assemble the TAI result, preserving the UTC split and order. */
#   a2 = z1 - u1;
#   a2 += z2;
#   a2 += fd + dat0/DAYSEC;
#   if ( big1 ) {
#      *tai1 = u1;
#      *tai2 = a2;
#   } else {
#      *tai1 = a2;
#      *tai2 = u1;
#   }
#
#/* Status. */
#   return j
#
#class UT1(Base):
#    def __init__(self, data ):
#        super().__init__(data)
#
#class UTC(Base):
#    def __init__(self, data ):
#        super().__init__(data)
#
#    def to_scale( self, scale : Scale ):
#
#        if scale == Scale.TAI:
#            return TAI.from_utc( scale.data )
#
