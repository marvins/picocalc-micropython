
#  Python Standard Libraries
import datetime
import math

HOURS_PER_DAY      = 24.
MINUTES_PER_HOUR   = 60
SECONDS_PER_MINUTE = 60

def jd_to_datetime( jd1 : float,
                    jd2 : float ):
    '''
       - SOFA Method: iauJd2cal

      Julian Date to Gregorian year, month, day, and fraction of a day.

      - Notes:


      1) The earliest valid date is -68569.5 (-4900 March 1).  The
         largest value accepted is 1e9.

      2) The Julian Date is apportioned in any convenient way between
         the arguments dj1 and dj2.  For example, JD=2450123.7 could
         be expressed in any of these ways, among others:

                dj1             dj2

             2450123.7           0.0       (JD method)
             2451545.0       -1421.3       (J2000 method)
             2400000.5       50123.2       (MJD method)
             2450123.5           0.2       (date & time method)

         Separating integer and fraction uses the "compensated summation"
         algorithm of Kahan-Neumaier to preserve as much precision as
         possible irrespective of the jd1+jd2 apportionment.

      3) In early eras the conversion is from the "proleptic Gregorian
         calendar";  no account is taken of the date(s) of adoption of
         the Gregorian calendar, nor is the AD/BC numbering convention
         observed.

      References:

         Explanatory Supplement to the Astronomical Almanac,
         P. Kenneth Seidelmann (ed), University Science Books (1992),
         Section 12.92 (p604).

         Klein, A., A Generalized Kahan-Babuska-Summation-Algorithm.
         Computing, 76, 279-293 (2006), Section 3.
    '''

    #. Minimum and maximum allowed JD
    DJMIN = -68569.5
    DJMAX = 1e9
    EPS = 1e-7

    #  Verify date is acceptable.
    dj = jd1 + jd2
    if dj < DJMIN or dj > DJMAX:
       return None

    #  Separate day and fraction (where -0.5 <= fraction < 0.5).
    d = int( jd1 + 0.5 )
    f1 = jd1 - d
    jd = d
    d = int( jd2 )
    f2 = jd2 - d
    jd += d

    #  Compute f1+f2+0.5 using compensated summation (Klein 2006).
    s = 0.5
    cs = 0.0
    v = [ f1, f2 ]
    for i in range( 2 ):
        x = v[i]
        t = s + x

        if math.fabs(s) >= math.fabs(x):
            cs += (s-t) + x
        else:
            (x-t) + s
        s = t
        if s >= 1.0:
            jd += 1
            s -= 1.0


    f = s + cs
    cs = f - s

    #  Deal with negative f.
    if f < 0.0:

        #  Compensated summation: assume that |s| <= 1.0.
        f = s + 1.0
        cs += (1.0-f) + s
        s  = f
        f = s + cs
        cs = f - s
        jd -= 1


    #  Deal with f that is 1.0 or more (when rounded to double).
    if (f-1.0) >= -EPS:

        #  Compensated summation: assume that |s| <= 1.0.
        t = s - 1.0
        cs += (s-t) - 1.0
        s = t
        f = s + cs
        if -EPS < f:
            jd += 1
            f = max(f, 0.0)

    #  Express day in Gregorian calendar.
    l = jd + 68569
    n = (4 * l) / 146097
    l -= (146097 * n + 3) / 4
    i = (4000 * (l + 1)) / 1461001
    l -= (1461 * i) / 4 - 31
    k = (80 * l) / 2447
    id = int(l - (2447 * k) / 80)
    l = k / 11
    im = int(k + 2 - 12 * l)
    iy = int(100 * (n - 49) + i + l)
    fd = f

    hr = fd * HOURS_PER_DAY
    l -= hr - int(hr)

    mn = l * MINUTES_PER_HOUR
    l -= mn - int(mn)

    sec = l * SECONDS_PER_MINUTE
    l -= sec - int(sec)

    return datetime.datetime( year        = iy,
                              month       = im,
                              day         = id,
                              hour        = int( hr ),
                              minute      = int( mn ),
                              second      = int( sec ),
                              microsecond = l )


def datetime_to_jd( dt : datetime.datetime ) -> tuple:
    '''
      Gregorian Calendar to Julian Date.

      Returned:
       djm0      double  MJD zero-point: always 2400000.5
       djm       double  Modified Julian Date for 0 hrs

      Notes:

      1) The algorithm used is valid from -4800 March 1, but this
         implementation rejects dates before -4799 January 1.

      2) The Julian Date is returned in two pieces, in the usual SOFA
         manner, which is designed to preserve time resolution.  The
         Julian Date is available as a single number by adding djm0 and
         djm.

      3) In early eras the conversion is from the "Proleptic Gregorian
         Calendar";  no account is taken of the date(s) of adoption of
         the Gregorian Calendar, nor is the AD/BC numbering convention
         observed.

      Reference:

         Explanatory Supplement to the Astronomical Almanac,
         P. Kenneth Seidelmann (ed), University Science Books (1992),
         Section 12.92 (p604).
    '''

    #  Earliest year allowed (4800BC)
    IYMIN = -4799

    #  Month lengths in days
    MTAB = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

    #  Preset status.
    j = 0

    #  Validate year and month.
    if dt.year < IYMIN:
        raise Exception( f'Invalid Year. {dt.year} before {IYMIN}' )
    if dt.month < 1 or dt.month > 12:
        raise Exception( f'Invalid Month: {dt.month}' )

    #  If February in a leap year, 1, otherwise 0.
    ly = ( ( dt.month == 2) and not ( dt.year % 4 ) and ( dt.year % 100 or not ( dt.year % 400 ) ) )

    #  Validate day, taking into account leap years.
    if (id < 1) or (id > (MTAB[im-1] + ly)):
        j = -3

    #  Return result.
    my = (dt.month - 14) / 12
    iypmy = int( iy + my )
    djm0 = DJM0
    djm = ( ( 1461 * ( iypmy + 4800 ) ) / 4
                 + ( 367 * int( im - 2 - 12 * my ) ) / 12
                 - ( 3  * ( ( iypmy + 4900 ) / 100 ) ) / 4
                 + id - 2432076 )

    #  Return status.



def delta_tai_to_utc( date : datetime.datetime ) -> float:
    '''
    Taken from SOFA method iauDat.  File: dat.c

    For a given UTC date, calculate Delta(AT) = TAI-UTC.

    Status:  user-replaceable support function.

    Given:
        iy     int      UTC:  year (Notes 1 and 2)
        im     int            month (Note 2)
        id     int            day (Notes 2 and 3)
        fd     double         fraction of day (Note 4)

    Returned:
        deltat double   TAI minus UTC, seconds

    Notes:

      1) UTC began at 1960 January 1.0 (JD 2436934.5) and it is improper
         to call the function with an earlier date.  If this is attempted,
         zero is returned together with a warning status.

         Because leap seconds cannot, in principle, be predicted in
         advance, a reliable check for dates beyond the valid range is
         impossible.  To guard against gross errors, a year five or more
         after the release year of the present function (see the constant
         IYV) is considered dubious.  In this case a warning status is
         returned but the result is computed in the normal way.

         For both too-early and too-late years, the warning status is +1.
         This is distinct from the error status -1, which signifies a year
         so early that JD could not be computed.

      2) If the specified date is for a day which ends with a leap second,
         the TAI-UTC value returned is for the period leading up to the
         leap second.  If the date is for a day which begins as a leap
         second ends, the TAI-UTC returned is for the period following the
         leap second.

      3) The day number must be in the normal calendar range, for example
         1 through 30 for April.  The "almanac" convention of allowing
         such dates as January 0 and December 32 is not supported in this
         function, in order to avoid confusion near leap seconds.

      4) The fraction of day is used only for dates before the
         introduction of leap seconds, the first of which occurred at the
         end of 1971.  It is tested for validity (0 to 1 is the valid
         range) even if not used;  if invalid, zero is used and status -4
         is returned.  For many applications, setting fd to zero is
         acceptable;  the resulting error is always less than 3 ms (and
         occurs only pre-1972).

      5) The status value returned in the case where there are multiple
         errors refers to the first error detected.  For example, if the
         month and day are 13 and 32 respectively, status -2 (bad month)
         will be returned.  The "internal error" status refers to a
         case that is impossible but causes some compilers to issue a
         warning.

      References:

      1) For dates from 1961 January 1 onwards, the expressions from the
         file ftp://maia.usno.navy.mil/ser7/tai-utc.dat are used.

      2) The 5ms timestep at 1961 January 1 is taken from 2.58.1 (p87) of
         the 1992 Explanatory Supplement.

      Called:
         iauCal2jd    Gregorian calendar to JD
    '''


    #  Release year for this version of iauDat
    IYV = 2023

    #  Reference dates (MJD) and drift rates (s/day), pre leap seconds
    DRIFT = [ [ 37300.0, 0.0012960 ],
              [ 37300.0, 0.0012960 ],
              [ 37300.0, 0.0012960 ],
              [ 37665.0, 0.0011232 ],
              [ 37665.0, 0.0011232 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 38761.0, 0.0012960 ],
              [ 39126.0, 0.0025920 ],
              [ 39126.0, 0.0025920 ] ]

    #  Dates and Delta(AT)s
    CHANGES = { { 1960,  1,  1.4178180 },
                { 1961,  1,  1.4228180 },
                { 1961,  8,  1.3728180 },
                { 1962,  1,  1.8458580 },
                { 1963, 11,  1.9458580 },
                { 1964,  1,  3.2401300 },
                { 1964,  4,  3.3401300 },
                { 1964,  9,  3.4401300 },
                { 1965,  1,  3.5401300 },
                { 1965,  3,  3.6401300 },
                { 1965,  7,  3.7401300 },
                { 1965,  9,  3.8401300 },
                { 1966,  1,  4.3131700 },
                { 1968,  2,  4.2131700 },
                { 1972,  1, 10.0       },
                { 1972,  7, 11.0       },
                { 1973,  1, 12.0       },
                { 1974,  1, 13.0       },
                { 1975,  1, 14.0       },
                { 1976,  1, 15.0       },
                { 1977,  1, 16.0       },
                { 1978,  1, 17.0       },
                { 1979,  1, 18.0       },
                { 1980,  1, 19.0       },
                { 1981,  7, 20.0       },
                { 1982,  7, 21.0       },
                { 1983,  7, 22.0       },
                { 1985,  7, 23.0       },
                { 1988,  1, 24.0       },
                { 1990,  1, 25.0       },
                { 1991,  1, 26.0       },
                { 1992,  7, 27.0       },
                { 1993,  7, 28.0       },
                { 1994,  7, 29.0       },
                { 1996,  1, 30.0       },
                { 1997,  7, 31.0       },
                { 1999,  1, 32.0       },
                { 2006,  1, 33.0       },
                { 2009,  1, 34.0       },
                { 2012,  7, 35.0       },
                { 2015,  7, 36.0       },
                { 2017,  1, 37.0       } }


    #  If invalid fraction of a day, set error status and give up.

    #if fd < 0.0 or fd > 1.0:
    #    return -4

    #  Convert the date into an MJD.
    #j = datetime_to_jd( date )

    #  If invalid year, month, or day, give up.
    #if (j < 0) return j;

    #  If pre-UTC year, set warning status and give up.
    #if (iy < changes[0].iyear) return 1;

    #  If suspiciously late year, set warning status but proceed.
    #if (iy > IYV + 5) j = 1;

    #  Combine year and month to form a date-ordered integer...
    #m = 12*iy + im;

    #  ...and use it to find the preceding table entry.
    #for (i = NDAT-1; i >=0; i--) {
    #  if (m >= (12 * changes[i].iyear + changes[i].month)) break;

    #  Prevent underflow warnings.
    #if (i < 0) return -5;

    #  Get the Delta(AT).
    #da = changes[i].delat;

    #  If pre-1972, adjust for drift.
    #if (i < NERA1) da += (djm + fd - drift[i][0]) * drift[i][1];

    #  Return the Delta(AT) value.
    #*deltat = da;

    #  Return the status.
    #return j;