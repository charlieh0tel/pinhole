#
# Copyright (c) 2023, Christopher Hoover
#
# SPDX-License-Identifier: BSD-3-Clause
#

"""Simple thin lens camera calculations."""

#
# References:
#
# Applied Photographic Optics, Third Edition, by Signey F. Ray.
#
# Depth of Field Outside the Box [[http://www.dicklyon.com/tech/Photography/DepthOfField-Lyon.pdf]]
#

import attr
import math
import numpy
import quantities as pq
import typing

INF = float("inf")


@attr.s(auto_attribs=True)
class Sensor:
    """Sensor."""

    name: str = ''
    pixel_pitch: pq.Quantity = None  # length
    width_pixels: int = None           # active area
    height_pixels: int = None          # activa area
    cfa: str = 'bayer'

    @property
    def sensor_width(self):
        """Returns the width of the sensor."""
        return self.pixel_pitch * self.width_pixels

    @property
    def sensor_height(self):
        """Returns the height of the sensor."""
        return self.pixel_pitch * self.height_pixels

    @property
    def sensor_diagonal(self):
        """Returns the length of the diagonal of the sensor."""
        return numpy.hypot(self.sensor_height, self.sensor_width)
        

    @property
    def circle_of_confusion_diameter(self):
        """Returns the diameter of the circle of confusion appropriate for the
           sensor.
        """

        if self.cfa == 'bayer':
            # Per Lyon, for Bayer sensor, the diameter C is then 2.25 pixels.
            return 2.25 * self.pixel_pitch
        else:
            raise Error('Unknown cfa \'%s\'', self.cfa)


@attr.s(auto_attribs=True)
class Lens:
    """Lens."""

    name: str = ''
    focal_length: pq.Quantity = None  # length
    aperture_diameter: pq.Quantity = None  # length
    projection: str = 'rectilinear'

    @property
    def f_number(self):
        return self.focal_length / self.aperture_diameter

    def _GetAngleOfView(self, focal_plane_length):
        if self.projection == 'rectilinear':
            return (
                2. * numpy.arctan2(
                    focal_plane_length,
                    2. * self.focal_length.rescale(focal_plane_length.units)) *
                pq.radian)
        elif self.projection == 'equidistant':
            angle = focal_plane_length / self.focal_length
            return angle.simplified * pq.radian
        else:
            raise Error('Unknown projection \'%s\'', self.projection)


@attr.s(auto_attribs=True)
class Camera(object):
    """Camera"""

    name: str = ''
    sensor: Sensor = None
    lens: Lens = None

    def GetAnglesOfView(self):
        """Returns the field (angles) of view."""
        return (self.lens._GetAngleOfView(self.sensor.sensor_width),
                self.lens._GetAngleOfView(self.sensor.sensor_height))

    def GetDiagonalAngleOfView(self):
        """Returns the diagonal field (angle) of view."""
        (angle_width, angle_height) = self.GetAnglesOfView()
        return numpy.hypot(angle_width, angle_height)

    def GetInstantaneousAngleOfView(self):
        """Returns the instantaneous field (angle) of view."""
        return self.lens._GetAngleOfView(self.sensor.pixel_pitch)

    def GetGroundSampleDistance(self, distance):
        """Returns the ground sample distance (GSD)."""
        ifov = self.GetInstantaneousAngleOfView()
        return 2. * distance * numpy.tan(ifov / 2.)

    def GetHyperfocalDistance(self):
        """Returns the hyperfocal distance."""
        focal_length = self.lens.focal_length
        focal_length_squared = focal_length * focal_length
        coc_diameter = self.sensor.circle_of_confusion_diameter

        hyperfocal_distance = (
            focal_length_squared /
            (self.lens.f_number * coc_diameter) + focal_length)

        return hyperfocal_distance.rescale(pq.meter)

    def GetDepthOfField(self, focus_distance):
        """Returns the (near, far) depth of field."""

        focal_length = self.lens.focal_length
        focal_length_squared = focal_length * focal_length

        assert focus_distance > self.lens.focal_length

        coc_diameter = self.sensor.circle_of_confusion_diameter

        # Equation 22.3
        near = (focus_distance * focal_length_squared /
                (focal_length_squared +
                 self.lens.f_number * coc_diameter * focus_distance))

        # Equation 22.4
        sd = (focal_length_squared -
              self.lens.f_number * coc_diameter * focus_distance)
        if sd > 0:
            far = focus_distance * focal_length_squared / sd
        else:
            far = INF * pq.m

        return (near, far)

    def Get35mmEquivalentFocalLength(self):
        """Returns the CIPA 35mm equivalent focal length."""
        # CIPA guidelines: "Converted focal length into
        # 35 mm camera" = (Diagonal distance of image area in the 35 mm
        # camera (43.27 mm) / Diagonal distance of image area on the
        # image sensor of the DSC) × focal length of the lens of the DSC.
        crop_factor = 43.27 * pq.mm / self.sensor.sensor_diagonal
        return (crop_factor * self.lens.focal_length).rescale(pq.mm)

    def GetAPSCEquivalentFocalLength(self):
        """Returns the APS C equivalent focal length."""
        return self.Get35mmEquivalentFocalLength() / 1.5
