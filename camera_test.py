#
# Copyright (c) 2023, Christopher Hoover
#
# SPDX-License-Identifier: BSD-3-Clause
#

"""Tests for camera.py"""

import numpy
import quantities as pq

from . import camera

def test_sensor():
    pitch = 1.55 * pq.micron
    w_px = 4096
    h_px = 3072
    sensor = camera.Sensor('s', pitch, w_px, h_px)
    assert sensor.sensor_width == pitch * w_px
    assert sensor.sensor_height == pitch * h_px
    assert sensor.circle_of_confusion_diameter == 2.25 * pitch


def test_lens():
    focal_length = 10 * pq.mm
    f_number = 2.
    aperture_diameter = focal_length / f_number
    lens = camera.Lens('l', focal_length, aperture_diameter)
    assert lens.f_number == f_number


def _ToRadians(x):
    return x.rescale(pq.radians)

def test_camera_rectilinear():
    pitch = 5 * pq.micron
    w_px = 4000
    h_px = 3000
    sensor = camera.Sensor('s', pitch, w_px, h_px)
    focal_length = 10 * pq.mm
    f_number = 2.
    aperture_diameter = focal_length / f_number
    lens = camera.Lens('l', focal_length, aperture_diameter)
    c = camera.Camera('c', sensor, lens)
    (horiz_angle, vert_angle) = c.GetAnglesOfView()
    assert numpy.isclose(horiz_angle, _ToRadians(90. * pq.degrees))
    assert numpy.isclose(vert_angle, _ToRadians(73.74 * pq.degrees),
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetDiagonalAngleOfView(), 2.03 * pq.radians,
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetInstantaneousAngleOfView(), 0.0005 * pq.radians,
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetGroundSampleDistance(1. * pq.meter),
                         0.000500 * pq.meter,
                         atol=0.000100 * pq.meter)
    assert numpy.isclose(c.GetHyperfocalDistance(),
                         4.45444444444 * pq.meter,
                         atol=0.01 * pq.meter)
    (near, far) = c.GetDepthOfField(1. * pq.meter)
    assert numpy.isclose(near, 0.8163 * pq.meter,
                         atol=0.01 * pq.meter)
    assert numpy.isclose(far, 1.29 * pq.meter,
                         atol=0.01 * pq.meter)
    assert numpy.isclose(c.Get35mmEquivalentFocalLength(),
                         17.31 * pq.mm,
                         atol=0.1 * pq.mm)
    assert numpy.isclose(c.GetAPSCEquivalentFocalLength(),
                         11.54 * pq.mm,
                         atol=0.1 * pq.mm)


def test_camera_equidistant():
    pitch = 5 * pq.micron
    w_px = 4000
    h_px = 3000
    sensor = camera.Sensor('s', pitch, w_px, h_px)
    focal_length = 10 * pq.mm
    f_number = 2.
    aperture_diameter = focal_length / f_number
    lens = camera.Lens('l', focal_length, aperture_diameter,
                       projection='equidistant')
    c = camera.Camera('c', sensor, lens)
    (horiz_angle, vert_angle) = c.GetAnglesOfView()
    assert numpy.isclose(horiz_angle, _ToRadians(114.6 * pq.degrees),
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(vert_angle, 85.944 * pq.degrees,
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetDiagonalAngleOfView(), 2.5 * pq.radians,
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetInstantaneousAngleOfView(), 0.0005 * pq.radians,
                         atol=_ToRadians(0.1 * pq.degrees))
    assert numpy.isclose(c.GetGroundSampleDistance(1. * pq.meter),
                         0.000500 * pq.meter,
                         atol=0.000100 * pq.meter)
    assert numpy.isclose(c.GetHyperfocalDistance(),
                         4.45444444444 * pq.meter,
                         atol=0.01 * pq.meter)
    (near, far) = c.GetDepthOfField(1. * pq.meter)
    assert numpy.isclose(near, 0.8163 * pq.meter,
                         atol=0.01 * pq.meter)
    assert numpy.isclose(far, 1.29 * pq.meter,
                         atol=0.01 * pq.meter)
    assert numpy.isclose(c.Get35mmEquivalentFocalLength(),
                         17.31 * pq.mm,
                         atol=0.1 * pq.mm)
    assert numpy.isclose(c.GetAPSCEquivalentFocalLength(),
                         11.54 * pq.mm,
                         atol=0.1 * pq.mm)
