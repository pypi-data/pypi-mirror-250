import spiceypy as spice
import numpy as np

def sun_px_angle(utc='', et=None):
    """
    Get the Sun-S/C +X Panel angle projected in the Plane normal to S/C +Y.

    Parameters
    ----------
    utc : str, optional
        UTC time format (default is '').
    et : float, optional
        Ephemeris Time (ET) in seconds past J2000 (default is None).

    Returns
    -------
    float
        The angle between the Sun-S/C +X Panel and the plane normal to S/C +Y in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))

    sc2sun, lt = spice.spkpos('SUN', et, 'JUICE_SPACECRAFT', 'NONE', 'JUICE')
    plane = spice.nvp2pl([0, 1, 0], [0, 0, 0])
    sc2sun_proj = spice.vhat(spice.vprjp(sc2sun, plane))
    ang = spice.vsep(sc2sun_proj, [1, 0, 0])
    return ang * spice.dpr()


def sun_pz_angle(utc='', et=None):
    """
    Get the Sun-S/C +Z Panel angle.

    Parameters
    ----------
    utc : str, optional
        UTC time format (default is '').
    et : float, optional
        Ephemeris Time (ET) in seconds past J2000 (default is None).

    Returns
    -------
    float
        The angle between the Sun-S/C +Z Panel and the positive z-axis in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))

    sc2sun, lt = spice.spkpos('SUN', et, 'JUICE_SPACECRAFT', 'NONE', 'JUICE')
    ang = spice.vsep(sc2sun, [0, 0, 1])
    return ang * spice.dpr()


def subsc_zsc_offset(utc='', et=None, target='GANYMEDE'):
    """
    Get the offset in between the sub-S/C point and the S/C +Z axis.

    Parameters
    ----------
    utc : str, optional
        UTC time format (default is '').
    et : float, optional
        Ephemeris Time (ET) in seconds past J2000 (default is None).
    target : str, optional
        Target celestial body (default is 'GANYMEDE').

    Returns
    -------
    float
        The offset angle between the sub-S/C point and the S/C +Z axis in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    target = target.upper()

    spoint, trgepc, srfvec = spice.subpnt('INTERCEPT/ELLIPSOID', target, et, f'IAU_{target}', 'NONE', 'JUICE')
    mat = spice.pxform('JUICE_SPACECRAFT', f'IAU_{target}', et)
    zsc = spice.mxv(mat, [0, 0, 1])
    ang = spice.vsep(zsc, srfvec)
    return ang * spice.dpr()


def target_zsc_offset(utc='', et=None, target='AMALTHEA'):
    """
    Get the offset in between a given target and the S/C +Z axis.

    Parameters
    ----------
    utc : str, optional
        UTC time format (default is '').
    et : float, optional
        Ephemeris Time (ET) in seconds past J2000 (default is None).
    target : str, optional
        Target celestial body (default is 'AMALTHEA').

    Returns
    -------
    float
        The offset angle between the given target and the S/C +Z axis in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    target = target.upper()

    spoint, trgepc, srfvec = spice.subpnt('INTERCEPT/ELLIPSOID', target, et, f'IAU_{target}', 'NONE', 'JUICE')
    mat = spice.pxform('JUICE_SPACECRAFT', f'IAU_{target}', et)
    zsc = spice.mxv(mat, [0, 0, 1])
    ang = spice.vsep(zsc, srfvec)
    return ang * spice.dpr()

def earth_direction(utc='', et=None, abcorr='NONE'):
    """
    Calculate the unit vector pointing from the spacecraft to Earth.

    Parameters
    ----------
    utc : str, optional
        UTC time format (default is '').
    et : float, optional
        Ephemeris Time (ET) in seconds past J2000 (default is None).
    abcorr : str, optional
        Aberration correction (default is 'NONE').

    Returns
    -------
    numpy.ndarray
        The unit vector pointing from the spacecraft to Earth in the spacecraft frame.
    """
    if utc:
        et = spice.utc2et(str(utc))
        # Calculate the spacecraft to Earth vector in the spacecraft frame
    sc2earth_vec, lt = spice.spkpos('EARTH', et, 'JUICE_SPACECRAFT', abcorr, 'JUICE')
    # Normalize the spacecraft to Earth vector
    return sc2earth_vec / np.linalg.norm(sc2earth_vec)


def sc_radec(utc='', et=None, axis=None, frame='ECLIPJ2000'):
    if axis is None:
        axis = [0, 0, 1]
    if utc:
        et = spice.utc2et(str(utc))
    mat = spice.pxform('JUICE_SPACECRAFT', frame, et)
    zsc = spice.mxv(mat, axis)
    range, ra, dec = spice.recrad(zsc)
    return ra * spice.dpr(), dec * spice.dpr()


def sc_boresight_angles(utc='', et=None, spacecraft_frame='JUICE_SPACECRAFT',
                        target_frame='J2000', boresight=None):
    if boresight is None:
        boresight = [0, 0, 1]
    if utc:
        et = spice.utc2et(str(utc))

    rot_mat = spice.pxform(spacecraft_frame, target_frame, et)
    euler = (spice.m2eul(rot_mat, 1, 2, 3))
    eul1 = np.degrees(euler[0])
    eul2 = np.degrees(euler[1])
    eul3 = np.degrees(euler[2])

    bsight = spice.mxv(rot_mat, boresight)
    bsight_angle = spice.vsep(bsight, boresight)
    bsight_angle = spice.convrt(bsight_angle, 'RADIANS', 'ARCSECONDS')

    (rot_axis, rot_angle) = spice.raxisa(rot_mat)
    rot_angle = spice.convrt(rot_angle, 'RADIANS', 'ARCSECONDS')

    return eul1, eul2, eul3, bsight_angle, rot_angle