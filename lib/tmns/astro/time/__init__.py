

#  Python Standard Libraries
import math

#  Terminus Astronomy Libraries
from tmns.astro.time.formats import ( Format,
                                      Julian_Date,
                                      Modified_Julian_Date,
                                      Seconds )
from tmns.astro.time.scales  import ( Scale,
                                      TAI )


class Time:

    def __init__(self, scale ):
        self.scale = scale

    @staticmethod
    def from_utc( jd_format : tuple = None ):

        #  If Julian specified
        if jd_format is not None:
            return Time( scale  = Scale.UTC,
                         format = Julian_Date( *jd_format ) )


    @staticmethod
    def decode( scale  : Scale,
                format : Format,
                value  : str ):
        '''
        Take an input from the user knowing the destination
        scale and format, and build the appropriate time object.
        '''
        formats = { Format.JD:      Julian_Date,
                    Format.MJD:     Modified_Julian_Date,
                    Format.SECONDS: Seconds }

        scales = { Scale.TAI:  TAI,
                   Scale.UT1:  UT1,
                   Scale.UTC:  UTC }

        return Time( scales[scale]( formats[format].from_string( value ) ) )
