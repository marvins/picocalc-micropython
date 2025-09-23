
#  Micropython Libraries
import logging

#  Terminus Astro Libraries
from tmns.astro import time

time_scale_config = {
    'title': 'Select Input Time Scale',
    'options': {
        '1': { 'name': 'UTC',
               'result': time.Scale.UTC },
        '2': { 'name': 'UT1',
               'result': time.Scale.UT1 },
        '3': { 'name': 'TAI',
               'result': time.Scale.TAI },
        'q': { 'name': 'Exit App',
               'result': 'exit' }
    }
}

time_format_config = {
    'title': 'Select Input Time Format',
    'options': {
        '1': { 'name': 'Julian Date',
               'result': time.Format.JD },
        '2': { 'name': 'Modified Julian Date',
               'result': time.Format.MJD },
        '3': { 'name': 'Seconds Since Epoch',
               'result': time.Format.SECONDS },
        '4': { 'name': 'ISO 8601',
               'result': time.Format.ISO_8601 },
        'q': { 'name': 'Exit App',
               'result': 'exit' }
    }
}

output_scale_config = {
    'title': 'Select Output Time Scale',
    'options': {
        '1': { 'name': 'UTC',
               'result': time.Scale.UTC },
        '2': { 'name': 'UT1',
               'result': time.Scale.UT1 },
        '3': { 'name': 'TAI',
               'result': time.Scale.TAI },
        'q': { 'name': 'Exit App',
               'result': 'exit' }
    }
}

def select_menu( config ):

    print( 'Time Converter' )
    print( '--------------' )
    print( '\n' )
    print( config['title'] )
    for opt in config['options'].keys():
        print( f'{opt}. {config["options"][opt]["name"]}' )
    res = input( ' --> Selection:' )

    for opt in config['options'].keys():
        if opt == res:
            return config['options'][opt]['result']

    return None

#  Main Program
def main( input_scale = None,
          input_format = None,
          input_value = None ):

    #  Time-scale input
    if input_scale is None:
        input_scale = select_menu( time_scale_config )
    else:
        input_scale = time.Scale.from_string( input_scale )
    if input_scale is None:
        raise Exception( 'Time scale query returned none.' )
    elif input_scale == 'exit':
        return

    #  Time-format input
    if input_format is None:
        input_format = select_menu( time_format_config )
    else:
        input_format = time.Format.from_string( input_format )
    if input_format is None:
        raise Exception( 'Time format query returned none.' )
    elif input_format == 'exit':
        return

    # Enter input value
    if input_value is None:
        input_value = input( 'Input Time Value: ' )

    input_time = time.Time.decode( input_scale,
                                   input_format,
                                   input_value )


    #  Output Time Scale
    output_scale = select_menu( output_scale_config )
    if output_scale is None:
        raise Exception( 'Output time scale query returned none.' )
    elif output_scale == 'exit':
        return

    #  Convert input time to output scale
    output_time = input_time.to_scale( output_scale )
