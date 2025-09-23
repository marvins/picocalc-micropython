
class Format:
    JD        = 'jd'
    MJD       = 'mjd'
    ISO_8601  = 'iso_8601'
    SECONDS   = 'seconds'

    @staticmethod
    def from_string( tp : str ):

        tp = str(tp).lower()
        if tp == Format.JD:
            return Format.JD
        if tp == Format.MJD:
            return Format.MJD
        if tp == Format.ISO_8601:
            return Format.ISO_8601
        if tp == Format.SECONDS:
            return Format.SECONDS
        return None

class Julian_Date:
    def __init__( self, jd1 : float, jd2 : float = 0 ):
        self.jd1 = jd1
        self.jd2 = jd2

    def single(self):
        return self.jd1 + self.jd2

class Modified_Julian_Date:

    def __init__( self, mjd ):
        pass

class Seconds:

    def __init__( self, secs ):
        self.seconds = list(secs)

    @staticmethod
    def from_string( value ):

        parts = str(value).split(' ')
        if len(parts) > 2:
            raise Exception( f'Bad input [{value}]' )
        return Seconds( [float(p) for p in parts] )


