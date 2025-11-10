#

#  Terminus astro has a few apps we'll pull in
import tmns.astro.apps.time_converter.main as tc
tmns_time_convert=tc.main
def test_time_convert():
    tmns_time_convert( 'utc', 'seconds', '1756948233' )

#  Browser App
import browser
file_browser=browser.file_browser

import test_dashboard as td

