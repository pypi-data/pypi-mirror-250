# -*- coding: utf-8 -*-

"""
    2017-01-01, 2016M, Jie Zheng
    Sun and Moon position function from IDL
"""


import numpy as np


# some trigonometric function with degree
_dsin_ = lambda a: np.sin(np.deg2rad(a))
_dcos_ = lambda a: np.cos(np.deg2rad(a))
_asind_ = lambda a: np.rad2deg(np.arcsin(a))
_atan2d_ = lambda a,b: np.rad2deg(np.arctan2(a, b))


def sun_pos(mjd):
    """ Compute sun position from jd, reference IDL astron
    args:
        jd: scalar or array of jd
    returns:
        ra, dec, longmed, oblt
        ra, dec: sun coord
        longmed - Ecliptic longitude of the sun at that date
        oblt - the obliquity of the ecliptic
    """
    # no list, list cannot do computing
    if type(mjd) is list: mjd = np.array(mjd)

    t = (mjd + 0.5 - 15020.0) / 36525.0  # original code is jd, so add 0.5

    #  form sun's mean longitude
    l = (279.696678 + ((36000.768925 * t) % 360.0)) * 3600.0

    #  allow for ellipticity of the orbit (equation of centre)
    #  using the Earth's mean anomaly ME
    me = 358.475844 + ((35999.049750 * t) % 360.0)
    ellcor  = (6910.1 - 17.2 * t) * _dsin_(me) + 72.3 * _dsin_(2.0 * me)
    l += ellcor

    # allow for the Venus perturbations using the mean anomaly of Venus MV

    mv = 212.603219 + ((58517.803875 * t) % 360.0)
    vencorr = (4.8 * _dcos_(299.1017 + mv - me) +
               5.5 * _dcos_(148.3133 +  2.0 * mv - 2.0 * me ) +
               2.5 * _dcos_(315.9433 +  2.0 * mv - 3.0 * me ) +
               1.6 * _dcos_(345.2533 +  3.0 * mv - 4.0 * me ) +
               1.0 * _dcos_(318.15   +  3.0 * mv - 5.0 * me ) )
    l += vencorr

    #  Allow for the Mars perturbations using the mean anomaly of Mars MM

    mm = 319.529425  +  (( 19139.858500 * t)  %  360.0 )
    marscorr = (2.0 * _dcos_(343.8883 - 2.0 * mm + 2.0 * me) +
                1.8 * _dcos_(200.4017 - 2.0 * mm + me) )
    l += marscorr

    # Allow for the Jupiter perturbations using the mean anomaly of Jupiter MJ

    mj = 225.328328  +  (( 3034.6920239 * t)  %  360.0 )
    jupcorr = (7.2 * _dcos_(179.5317 - mj + me ) +
               2.6 * _dcos_(263.2167 - mj ) +
               2.7 * _dcos_( 87.1450 - 2.0 * mj + 2.0 * me ) +
               1.6 * _dcos_(109.4933 - 2.0 * mj + me ) )
    l += jupcorr

    # Allow for the Moons perturbations using the mean elongation of the Moon from the Sun D

    d = 350.7376814  + (( 445267.11422 * t)  %  360.0 )
    mooncorr  = 6.5 * _dsin_(d)
    l += mooncorr

    # Allow for long period terms

    longterm = + 6.4 * _dsin_(231.19 + 20.20 * t)
    l += longterm
    l = (l + 2592000.0) % 1296000.0
    longmed = l / 3600.0

    # Allow for Aberration

    l -= 20.5

    # Allow for Nutation using the longitude of the Moons mean node OMEGA

    omega = 259.183275 - (( 1934.142008 * t ) % 360.0)
    l -= 17.2 * _dsin_(omega)

    # Form the True Obliquity

    oblt = 23.452294 - 0.0130125 * t + (9.2 * _dcos_(omega)) / 3600.0

    # Form Right Ascension and Declination

    l /= 3600.0
    ra = _atan2d_( _dsin_(l) * _dcos_(oblt), _dcos_(l) ) % 360.0
    dec = _asind_( _dsin_(l) * _dsin_(oblt) )

    return ra, dec, longmed, oblt


def moon_pos(mjd):
    """ Compute moon position from jd, reference IDL astron
    args:
        jd: scalar or array of jd
    returns:
        ra, dec, dis, geolong, geolat

        ra, dec: the coord of the moon
        dis : the Earth-moon distance in kilometers
        geolong, geolat: apparent longitude and latitude of the moon
    """
    # no list, list cannot do computing
    if type(mjd) is list:
        mjd = np.array(mjd)
    elif type(mjd) is not np.ndarray:
        mjd = np.array([mjd], dtype=float)
    n_jd = len(mjd)

    #  form time in julian centuries from 1900.0
    t = (mjd + 0.5 - 51545.0) / 36525.0  # original code is jd, so +0.5

    d_lng = np.array([0,2,2,0,0,0,2,2,2,2,0,1,0,2,0,0,4,0,4,2,2,1,1,2,2,4,2,0,2,2,1,2,0,0,
                      2,2,2,4,0,3,2,4,0,2,2,2,4,0,4,1,2,0,1,3,4,2,0,1,2,2])

    m_lng = np.array([0,0,0,0,1,0,0,-1,0,-1,1,0,1,0,0,0,0,0,0,1,1,0,1,-1,0,0,0,1,0,-1,0,
                      -2,1,2,-2,0,0,-1,0,0,1,-1,2,2,1,-1,0,0,-1,0,1,0,1,0,0,-1,2,1,0,0])

    mp_lng = np.array([1,-1,0,2,0,0,-2,-1,1,0,-1,0,1,0,1,1,-1,3,-2,-1,0,-1,0,1,2,0,-3,-2,
                      -1,-2,1,0,2,0,-1,1,0,-1,2,-1,1,-2,-1,-1,-2,0,1,4,0,-2,0,2,1,-2,-3,2,1,-1,
                      3,-1])

    f_lng = np.array([0,0,0,0,0,2,0,0,0,0,0,0,0,-2,2,-2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,
                      0,0,0,-2,2,0,2,0,0,0,0,0,0,-2,0,0,0,0,-2,-2,0,0,0,0,0,0,0,-2])

    sin_lng = np.array([6288774,1274027,658314,213618,-185116,-114332,58793,57066,53322,
                        45758,-40923,-34720,-30383,15327,-12528,10980,10675,10034,8548,-7888,-6766,
                        -5163,4987,4036,3994,3861,3665,-2689,-2602,2390,-2348,2236,-2120,-2069,2048,
                        -1773,-1595,1215,-1110,-892,-810,759,-713,-700,691,596,549,537,520,-487,
                        -399,-381,351,-340,330,327,-323,299,294,0.0])

    cos_lng = np.array([-20905355,-3699111,-2955968,-569925,48888,-3149,246158,-152138,
                        -170733,-204586,-129620,108743,104755,10321,0,79661,-34782,-23210,-21636,
                        24208,30824,-8379,-16675,-12831,-10445,-11650,14403,-7003,0,10056,6322,
                        -9884,5751,0,-4950,4130,0,-3958,0,3258,2616,-1897,-2117,2354,0,0,-1423,
                        -1117,-1571,-1739,0,-4421,0,0,0,0,1165,0,0,8752.0])

    d_lat = np.array([0,0,0,2,2,2,2,0,2,0,2,2,2,2,2,2,2,0,4,0,0,0,1,0,0,0,1,0,4,4,0,4,2,2,
                      2,2,0,2,2,2,2,4,2,2,0,2,1,1,0,2,1,2,0,4,4,1,4,1,4,2])

    m_lat = np.array([0,0,0,0,0,0,0,0,0,0,-1,0,0,1,-1,-1,-1,1,0,1,0,1,0,1,1,1,0,0,0,0,0,0,
                      0,0,-1,0,0,0,0,1,1,0,-1,-2,0,1,1,1,1,1,0,-1,1,0,-1,0,0,0,-1,-2])

    mp_lat = np.array([0,1,1,0,-1,-1,0,2,1,2,0,-2,1,0,-1,0,-1,-1,-1,0,0,-1,0,1,1,0,0,3,0,
                       -1,1, -2,0,2,1,-2,3,2,-3,-1,0,0,1,0,1,1,0,0,-2,-1,1,-2,2,-2,-1,1,1,-1,0,0])

    f_lat = np.array([1,1,-1,-1,1,-1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,-1,-1,1,3,1,1,1,-1,-1,-1,
                      1,-1,1,-3,1,-3,-1,-1,1,-1,1,-1,1,1,1,1,-1,3,-1,-1,1,-1,-1,1,-1,1,-1,-1,
                      -1,-1,-1,-1,1])

    sin_lat = np.array([5128122,280602,277693,173237,55413,46271,32573,17198,9266,8822,
                        8216,4324,4200,-3359,2463,2211,2065,-1870,1828,-1794,-1749,-1565,-1491,
                        -1475,-1410,-1344,-1335,1107,1021,833,777,671,607,596,491,-451,439,422,
                        421,-366,-351,331,315,302,-283,-229,223,223,-220,-220,-185,181,-177,176,
                        166,-164,132,-119,115,107.0])

    # mean longitude of the moon referred to mean equinox of the date
    coeff0 = [218.3164477, 481267.88123421, -0.0015786, 1.0/538841.0, -1.0/6.5194e7]
    coeff0.reverse()
    lprimed = np.polyval(coeff0, t) % 360.0
    lprime = np.deg2rad(lprimed)

    # mean elongation of the moon
    coeff1 = [297.8501921, 445267.1114034, -0.0018819, 1.0/545868.0, -1.0/1.13065e8]
    coeff1.reverse()
    d = np.deg2rad(np.polyval(coeff1, t) % 360.0)

    # sun's mean anomaly
    coeff2 = [357.5291092, 35999.0502909, -0.0001536, 1.0/2.449e7]
    coeff2.reverse()
    m = np.deg2rad(np.polyval(coeff2, t) % 360.0)

    # moon's mean anomaly
    coeff3 = [134.9633964, 477198.8675055, 0.0087414, 1.0/6.9699e4, -1.0/1.4712e7]
    coeff3.reverse()
    mprime = np.deg2rad(np.polyval(coeff3, t) % 360.0)

    # moon's argument of latitude
    coeff4 = [93.2720950, 483202.0175233, -0.0036539, -1.0/3.526e7, 1.0/8.6331e8]
    coeff4.reverse()
    f = np.deg2rad(np.polyval(coeff4, t) % 360.0)

    # eccentricity of earth's orbit around the sun
    e = 1 - 0.002516 * t - 7.4e-6 * t * t
    e2 = e * e

    ecorr1 = np.where(np.abs(m_lng) == 1)[0]
    ecorr2 = np.where(np.abs(m_lat) == 1)[0]
    ecorr3 = np.where(np.abs(m_lng) == 2)[0]
    ecorr4 = np.where(np.abs(m_lat) == 2)[0]

    # additional arguments

    a1 = np.deg2rad(119.75 +    131.849 * t)
    a2 = np.deg2rad( 53.09 + 479264.290 * t)
    a3 = np.deg2rad(313.45 + 481266.484 * t)
    suml_add = 3958.0 * np.sin(a1) + 1962.0 * np.sin(lprime - f) + 318.0 * np.sin(a2)
    sumb_add = (-2235.0 * np.sin(lprime) + 382.0 * np.sin(a3) + 175.0 * np.sin(a1-f) +
                175.0 * np.sin(a1 + f) + 127.0 * np.sin(lprime - mprime) -
                115.0 * np.sin(lprime + mprime) )

    # sum the periodic terms
    geolong = np.empty(n_jd, dtype=float)
    geolat  = np.empty(n_jd, dtype=float)
    dis     = np.empty(n_jd, dtype=float)

    for i in range(n_jd):
        sinlng = sin_lng.copy()
        coslng = cos_lng.copy()
        sinlat = sin_lat.copy()

        sinlng[ecorr1] *= e[i]
        coslng[ecorr1] *= e[i]
        sinlat[ecorr2] *= e[i]
        sinlng[ecorr3] *= e2[i]
        coslng[ecorr3] *= e2[i]
        sinlat[ecorr4] *= e2[i]

        arg = d_lng * d[i] + m_lng * m[i] + mp_lng * mprime[i] + f_lng * f[i]
        geolong[i] = lprimed[i] + (np.sum(sinlng * np.sin(arg)) + suml_add[i]) / 1.0e6

        dis[i] = 385000.56 + np.sum(coslng * np.cos(arg)) / 1.0e3

        arg = d_lat * d[i] + m_lat * m[i] + mp_lat * mprime[i] + f_lat * f[i]
        geolat[i] = (np.sum(sinlat * np.sin(arg)) + sumb_add[i]) / 1.0e6

    nlong, elong = nutate(mjd)                      # find the nutation in longitude

    geolong += nlong / 3600.0
    geolong %= 360.0
    lamb = np.deg2rad(geolong)
    beta = np.deg2rad(geolat)

    #find mean obliquity and convert lamb,beta to ra, dec

    c = [21.448,-4680.93,-1.55,1999.25,-51.38,-249.67,-39.05,7.12,27.87,5.79,2.45]
    c.reverse()
    epsilon = (23.0 + 26.0/60.0) + np.polyval(c, t / 100.0) / 3600.0
    eps = np.deg2rad(epsilon + elong / 3600.0 )          #true obliquity in radians

    ra = _atan2d_(
        np.sin(lamb) * np.cos(eps) - np.tan(beta) * np.sin(eps), np.cos(lamb) ) % 360.0
    dec = _asind_( np.sin(beta) * np.cos(eps) + np.cos(beta) * np.sin(eps) * np.sin(lamb) )

    if n_jd == 1:
        return ra[0], dec[0], dis[0], geolong[0], geolat[0]
    else:
        return ra, dec, dis, geolong, geolat


def nutate(mjd):
    """ Compute the nutation in longitude and obliquity for a given Julian date, reference IDL astron
        used in moonpos
    args:
        jd: scalar or array of jd
    returns:
        nut_long, nut_obliq: the nutation in longitude and latitude
    """
    # no list, list cannot do computing
    if type(mjd) is list:
        mjd = np.array(mjd)
    elif type(mjd) is not np.ndarray:
        mjd = np.array([mjd], dtype=float)
    n_jd = len(mjd)

    #  form time in Julian centuries from 1900.0

    t = (mjd + 0.5 - 51545.0) / 36525.0  # original code is jd, so +0.5


    # Mean elongation of the Moon
    coeff1 = [297.85036,  445267.111480, -0.0019142, 1.0/189474]
    coeff1.reverse()
    d = np.deg2rad(np.polyval(coeff1, t) % 360.0)

    # Sun's mean anomaly
    coeff2 = [357.52772, 35999.050340, -0.0001603, -1.0/3e5]
    coeff2.reverse()
    m = np.deg2rad(np.polyval(coeff2, t) % 360.0)

    # Moon's mean anomaly
    coeff3 = [134.96298, 477198.867398, 0.0086972, 1.0/5.625e4 ]
    coeff3.reverse()
    mprime = np.deg2rad(np.polyval(coeff3, t) % 360.0)

    # Moon's argument of latitude
    coeff4 = [93.27191, 483202.017538, -0.0036825, -1.0/3.27270e5 ]
    coeff4.reverse()
    f = np.deg2rad(np.polyval(coeff4, t) % 360.0)

    # Longitude of the ascending node of the Moon's mean orbit on the ecliptic,
    #  measured from the mean equinox of the date
    coeff5 = [125.04452, -1934.136261, 0.0020708, 1.0/4.5e5]
    coeff5.reverse()
    omega = np.deg2rad(np.polyval(coeff5, t) % 360.0)

    d_lng = np.array([0,-2,0,0,0,0,-2,0,0,-2,-2,-2,0,2,0,2,0,0,-2,0,2,0,0,-2,0,-2,0,0,2,
                      -2,0,-2,0,0,2,2,0,-2,0,2,2,-2,-2,2,2,0,-2,-2,0,-2,-2,0,-1,-2,1,0,0,-1,0,0,
                      2,0,2])

    m_lng = np.array([0,0,0,0,1,0,1,0,0,-1]+[0]*17+[2,0,2,1,0,-1,0,0,0,1,1,-1,0,
                      0,0,0,0,0,-1,-1,0,0,0,1,0,0,1,0,0,0,-1,1,-1,-1,0,-1])

    mp_lng = np.array([0,0,0,0,0,1,0,0,1,0,1,0,-1,0,1,-1,-1,1,2,-2,0,2,2,1,0,0,-1,0,-1,
                       0,0,1,0,2,-1,1,0,1,0,0,1,2,1,-2,0,1,0,0,2,2,0,1,1,0,0,1,-2,1,1,1,-1,3,0])

    f_lng = np.array([0,2,2,0,0,0,2,2,2,2,0,2,2,0,0,2,0,2,0,2,2,2,0,2,2,2,2,0,0,2,0,0,
                      0,-2,2,2,2,0,2,2,0,2,2,0,0,0,2,0,2,0,2,-2,0,0,0,2,2,0,0,2,2,2,2])

    om_lng = np.array([1,2,2,2,0,0,2,1,2,2,0,1,2,0,1,2,1,1,0,1,2,2,0,2,0,0,1,0,1,2,1,
                       1,1,0,1,2,2,0,2,1,0,2,1,1,1,0,1,1,1,1,1,0,0,0,0,0,2,0,0,2,2,2,2])

    sin_lng = np.array([-171996, -13187, -2274, 2062, 1426, 712, -517, -386, -301, 217,
                        -158, 129, 123, 63, 63, -59, -58, -51, 48, 46, -38, -31, 29, 29, 26, -22,
                        21, 17, 16, -16, -15, -13, -12, 11, -10, -8, 7, -7, -7, -7,
                        6,6,6,-6,-6,5,-5,-5,-5,4,4,4,-4,-4,-4,3,-3,-3,-3,-3,-3,-3,-3 ])

    sdelt = np.array([-174.2, -1.6, -0.2, 0.2, -3.4, 0.1, 1.2, -0.4, 0, -0.5, 0, 0.1,
                      0,0,0.1, 0,-0.1]+[0.0]*10+[-0.1, 0, 0.1]+[0.0]*33)

    cos_lng = np.array([92025, 5736, 977, -895, 54, -7, 224, 200, 129, -95,0,-70,-53,0,
                        -33, 26, 32, 27, 0, -24, 16,13,0,-12,0,0,-10,0,-8,7,9,7,6,0,5,3,-3,0,3,3,
                        0,-3,-3,3,3,0,3,3,3]+[0]*14)

    cdelt = np.array([8.9, -3.1, -0.5, 0.5, -0.1, 0.0, -0.6, 0.0, -0.1, 0.3]+[0.0]*53)

    # Sum the periodic terms
    nut_long = np.empty(n_jd)
    nut_obliq = np.empty(n_jd)

    #mul = lambda aa, bb: np.matmul(np.array([aa]).T,[bb])

    arg = mul(d_lng, d) + mul(m_lng, m) + mul(mp_lng, mprime) + mul(f_lng, f) + mul(om_lng, omega)
    sarg = np.sin(arg)
    carg = np.cos(arg)
    for i in range(n_jd):
        nut_long[i] =  0.0001 * np.sum( (sdelt * t[i] + sin_lng) * sarg[:,i] )
        nut_obliq[i] = 0.0001 * np.sum( (cdelt * t[i] + cos_lng) * carg[:,i] )

    return nut_long, nut_obliq


def mul(aa, bb):
    """a simulated matrix mul function, only for vector X vector
    args:
        aa, bb: n and m items vector
    returns:
        aa x bb
    """
    na, nb = len(aa), len(bb)
    res = np.empty([na, nb])
    for a in range(na):
        res[a] = aa[a] * bb
    return res


def moon_phase (mjd) :
    """ get moon phase at given time
        method from MPHASE.pro in astron lib for IDL
    """
    diss = 1.49598e8         # Earth-Sun distance (1 AU)

    ram, decm, dism, lonm, latm = moon_pos(mjd)
    ras, decs, lons, oblts = sun_pos(mjd)

    # phi - geocentric elongation of the Moon from the Sun
    # inc - selenocentric (Moon centered) elongation of the Earth from the Sun
    phi = np.arccos( _dsin_(decs) * _dsin_(decm) +
                     _dcos_(decs) * _dcos_(decm) * _dcos_(ras - ram) )
    inc = np.arctan2(diss * np.sin(phi), dism - diss * np.cos(phi))
    p = (1 + np.cos(inc)) / 2.0
    return p


def moon_phase2 (yr, mn, dy, hr=0, mi=0, se=0, tz=0) :
    """ get moon phase at given time
    https://www.daniweb.com/programming/software-development/code/453788/moon-phase-at-a-given-date-python
    args:
        yr: year
        mn: month
        dy: day
        hr: hour
        mi: minute
        se: second
        tz: timezone
    returns:
        moonphase, 0.0 to 1.0
    """
    hh = hr + mi / 60.0 + se / 3600.0 - tz
    year_corr = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    month_corr = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    lunar_day = (year_corr[(yr + 1) % 19] + month_corr[mn-1] + dy + hh) % 30.0
    phase = 2.0 * lunar_day / 29.0
    if phase > 1.0:
        phase = abs(phase - 2.0)
    return phase
