import spiceypy as spice

def jupiter_altitude_limit(altitude=1000):
    """
    Set the altitude limit for occultation above the 1 bar level of Jupiter.

    Parameters
    ----------
    altitude : int or float, optional
        Altitude value to be added to the 1 bar level (default: 1000).

    Returns
    -------
    numpy.ndarray
        Updated ellipsoid radii of Jupiter.
    """
    radii = spice.gdpool("BODY599_RADII", 0, 3)
    radii += altitude
    spice.pdpool("BODY599_RADII", radii)

    return radii