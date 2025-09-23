
from collections import namedtuple

from tmns.astro.const import DAS2R

IAU_00_Bias = namedtuple( 'IAU_00_Bias', [ 'dpsibi',
                                           'depsbi',
                                           'dra' ] )

class IAU_2000_Model:

    @staticmethod
    def bias_components() -> IAU_00_Bias:
        '''
        Frame bias components of IAU 2000 precession-nutation models; part
        of the Mathews-Herring-Buffett (MHB2000) nutation series, with
        additions.

        Returns:
        - dpsibi,depsbi  longitude and obliquity corrections
        - dra            the ICRS RA of the J2000.0 mean equinox

        SOFA Notes:

         1) The frame bias corrections in longitude and obliquity (radians)
            are required in order to correct for the offset between the GCRS
            pole and the mean J2000.0 pole.  They define, with respect to the
            GCRS frame, a J2000.0 mean pole that is consistent with the rest
            of the IAU 2000A precession-nutation model.

        2) In addition to the displacement of the pole, the complete
           description of the frame bias requires also an offset in right
           ascension.  This is not part of the IAU 2000A model, and is from
           Chapront et al. (2002).  It is returned in radians.

        3) This is a supplemented implementation of one aspect of the IAU
           2000A nutation model, formally adopted by the IAU General
           Assembly in 2000, namely MHB2000 (Mathews et al. 2002).

        References:

           Chapront, J., Chapront-Touze, M. & Francou, G., Astron.
           Astrophys., 387, 700, 2002.

           Mathews, P.M., Herring, T.A., Buffet, B.A., "Modeling of nutation
           and precession:  New nutation series for nonrigid Earth and
           insights into the Earth's interior", J.Geophys.Res., 107, B4,
           2002.  The MHB2000 code itself was obtained on 2002 September 9
           from ftp://maia.usno.navy.mil/conv2000/chapter5/IAU2000A.
        '''

        #  The frame bias corrections in longitude and obliquity
        DPBIAS = -0.041775  * DAS2R
        DEBIAS = -0.0068192 * DAS2R

        #  The ICRS RA of the J2000.0 equinox (Chapront et al., 2002)
        DRA0 = -0.0146 * DAS2R

        return IAU_00_Bias( DPBIAS,
                            DEBIAS,
                            DRA0 )

    def bias( time : Time ):
        '''
        Frame bias and precession, IAU 2000.

        This function is part of the International Astronomical Union's
        SOFA (Standards of Fundamental Astronomy) software collection.

        Status:  canonical model.

        Given:
            date1,date2  double         TT as a 2-part Julian Date (Note 1)

        Returned:
           rb           double[3][3]   frame bias matrix (Note 2)
           rp           double[3][3]   precession matrix (Note 3)
           rbp          double[3][3]   bias-precession matrix (Note 4)

        Notes:

        1) The TT date date1+date2 is a Julian Date, apportioned in any
           convenient way between the two arguments.  For example,
           JD(TT)=2450123.7 could be expressed in any of these ways,
           among others:

                   date1         date2

               2450123.7           0.0       (JD method)
               2451545.0       -1421.3       (J2000 method)
               2400000.5       50123.2       (MJD method)
               2450123.5           0.2       (date & time method)

           The JD method is the most natural and convenient to use in
           cases where the loss of several decimal digits of resolution
           is acceptable.  The J2000 method is best matched to the way
           the argument is handled internally and will deliver the
           optimum resolution.  The MJD method and the date & time methods
           are both good compromises between resolution and convenience.

        2) The matrix rb transforms vectors from GCRS to mean J2000.0 by
           applying frame bias.

        3) The matrix rp transforms vectors from J2000.0 mean equator and
           equinox to mean equator and equinox of date by applying
           precession.

        4) The matrix rbp transforms vectors from GCRS to mean equator and
           equinox of date by applying frame bias then precession.  It is
           the product rp x rb.

        5) It is permissible to re-use the same array in the returned
           arguments.  The arrays are filled in the order given.

        Called:
           iauBi00      frame bias components, IAU 2000
           iauPr00      IAU 2000 precession adjustments
           iauIr        initialize r-matrix to identity
           iauRx        rotate around X-axis
           iauRy        rotate around Y-axis
           iauRz        rotate around Z-axis
           iauCr        copy r-matrix
           iauRxr       product of two r-matrices

        Reference:
           "Expressions for the Celestial Intermediate Pole and Celestial
           Ephemeris Origin consistent with the IAU 2000A precession-
           nutation model", Astron.Astrophys. 400, 1145-1154 (2003)

           n.b. The celestial ephemeris origin (CEO) was renamed "celestial
                intermediate origin" (CIO) by IAU 2006 Resolution 2.
        '''

        #  J2000.0 obliquity (Lieske et al. 1977)
        EPS0 = 84381.448 * DAS2R

        #  Interval between fundamental epoch J2000.0 and current date (JC)
        t = ((date1 - DJ00) + date2) / DJC

        #  Frame bias.
        comps = IAU_00_Bias.bias_components()
        #iauBi00(&dpsibi, &depsbi, &dra0);

        #  Precession angles (Lieske et al. 1977)
        psia77 = (5038.7784 + (-1.07259 + (-0.001147) * t) * t) * t * DAS2R
        oma77  =       EPS0 + ((0.05127 + (-0.007726) * t) * t) * t * DAS2R
        chia   = (  10.5526 + (-2.38064 + (-0.001125) * t) * t) * t * DAS2R

        #  Apply IAU 2000 precession corrections.
        iauPr00(date1, date2, &dpsipr, &depspr)
        psia = psia77 + dpsipr
        oma  = oma77  + depspr

        #  Frame bias matrix: GCRS to J2000.0.
        iauIr(rbw)
        iauRz(dra0, rbw)
        iauRy(dpsibi*sin(EPS0), rbw)
        iauRx(-depsbi, rbw)
        iauCr(rbw, rb)

        #  Precession matrix: J2000.0 to mean of date.
        iauIr(rp)
        iauRx(EPS0, rp)
        iauRz(-psia, rp)
        iauRx(-oma, rp)
        iauRz(chia, rp)

        #  Bias-precession matrix: GCRS to mean of date.
        iauRxr(rp, rbw, rbp);

