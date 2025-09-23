#!/usr/bin/env python3

import numpy as np

from scipy.spatial.transform import Rotation as R

def test_quaternion_zyx():

    q1 = R.from_euler( 'Z', [45], degrees = True )

    M1 = q1.as_matrix()

    print( f'Result: {M1 @ np.array([[1],[0],[0]])}' )


test_quaternion_zyx()