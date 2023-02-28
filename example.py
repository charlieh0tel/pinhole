#!/usr/bin/python3

#
# Copyright (c) 2023, Christopher Hoover
#
# SPDX-License-Identifier: BSD-3-Clause
#

import numpy as np
import quantities as pq
import sys

import camera

def main(argv):
    # IMX[345]77
    pitch = 1.55 * pq.micron
    w_px = 4096
    h_px = 3072
    sensor = camera.Sensor('s', pitch, w_px, h_px)
    print(f";{sensor}")

    distance = 25. * pq.meter

    for l in [1., 2., 3., 3.5, 4, 4.5, 5, 5.5, 6.]:
        focal_length = l * pq.mm
        f_number = 2.
        aperture_diameter = focal_length / f_number
        lens = camera.Lens('l', focal_length, aperture_diameter)
        c = camera.Camera('c', sensor, lens)
        focal_length_35mm = c.Get35mmEquivalentFocalLength()
        (horiz_angle, vert_angle) = c.GetAnglesOfView()
        solid_angle = horiz_angle * vert_angle
        horiz_angle = horiz_angle.rescale(pq.degrees)
        vert_angle = vert_angle.rescale(pq.degrees)
        dfov = c.GetDiagonalAngleOfView().rescale(pq.degrees)
        ifov = c.GetInstantaneousAngleOfView().rescale(pq.degrees)
        hyperfocal = c.GetHyperfocalDistance()
        (near, far) = c.GetDepthOfField(distance)
        gsd = c.GetGroundSampleDistance(distance)

        print()
        print(f"focal_length: {focal_length} "
              f"({focal_length_35mm:.0f} equiv for 35 mm)")
        print(f"fov: {horiz_angle:.0f} x {vert_angle:.0f}")
        print(f"solid angle: {solid_angle:.3f}")
        print(f"dfov: {dfov:.3f}")
        print(f"ifov: {ifov:.3f}")
        print(f"gsd: {gsd.rescale(pq.mm):.3f}")
        print(f"hyperfocal: {hyperfocal:.0f}")
        print(f"near: {near:.0f}")
        print(f"far: {far:.0f}")

if __name__ == "__main__":
    main(sys.argv)
