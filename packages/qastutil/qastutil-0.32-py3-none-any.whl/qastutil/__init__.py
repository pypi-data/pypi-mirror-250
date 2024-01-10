"""
收集汇总自己以前各个项目用到的小工具函数，避免重复造轮子

v1: 2022-10-18

- dec2dms: transfer decimal to sexagesimal deg-min-sec, for Dec
- dec2hms: transfer decimal to sexagesimal hour-min-sec, for RA
- dms2dec: transfer sexagesimal deg-min-sec to decimal, for Dec
- hms2dec: transfer sexagesimal hour-min-sec to decimal, for RA
- coorddec2dms: transfer astropy.coord.dec to deg-min-sec
- coordra2hms: transfer astropy.coord.ra to hour-min-sec
- hour2str: transfer decimal hour to hour-min-sec
- hourangle: computer hour angle between lst and ra
- angle_dis: distance between two angles, result between -180 and +180
- distance: distance between two sphere points
- azalt: az & alt for object (ra, dec) at lat, lst
- mjd: from y, m, d, h, s, s, tz to mjd
- day_of_year: day serial number in given year
- fmst: fast midnight sidereal time
- mjd2: from y, m, d, h, s, s, tz to mjd
- night_len: n of hours from sunset to sunrise
- night_time: sunset and sunrise for given yr, mn, dy, lon, lat, tz
- mjd_of_night: get 4-digit mjd code for the site, using local 18:00
- mjd2hour: Extract hour part from mjd
- sun_action: Get time of sun pass specified altitude, in this night
- airmass: airmass from lat, lst, ra, dec
- lst: get local sidereal time for longitude at mjd, no astropy
- sun_pos: sun position of given mjd
- moon_pos: moon position of given mjd
- moon_phase: moon phase of given mjd, by sun-earth-moon angle
- moon_phase2: moon phase by moon cycle

"""


from .angle import dec2dms, dec2hms, dms2dec, hms2dec, coorddec2dms, coordra2hms, hour2str, hourangle, angle_dis
from .sky import distance, azalt, mjd, day_of_year, fmst, mjd2, night_len, \
    night_time, mjd_of_night, mjd2hour, sun_action, airmass, lst
from .sunmoon import sun_pos, moon_pos, moon_phase, moon_phase2
