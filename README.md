# SARAO Archive Tool

This tool is designed to produce summary statistics for an observation on the SARAO archive, especially LADUMA/MeerKAT tracks. The following outputs are given for each observing log:
- Observation Season
- Track Number and Frequency Band (e.g. L35)
- Observation Date
- Schedule Block
- Capture Block
- Target Name
- Target RA
- Target Declination
- Dump Rate (Hz)
- Dataset Size (GB)
- Number of MeerKAT Antennas Used
- Missing Antennas (separated with hypens e.g. `m16- m22- m37`)
- Total On- Source Time
- Initial Source Hour Angle (decimal hours)
- Final Source Hour Angle (decimal hours)
- Spectral Band
- SPW Product
- SPW Center Frequency (MHz)
- SPW Bandwidth (MHz)
- SPW Number of Channels
- SPW Channel Width (kHz)

To run the code, place all the log files (plain text directory) and run the program. It will prompt for the path to this directory. It will then save the summary statistics to a CSV file in that directory.

### Important Notes
1. This program assumes that there is only one SPW per observation log. If there is more than one, the SPW summary statistics (e.g. `spwBand`) will reflect only the first of the SPWs. 
2. Source hour angles are calculated using the source RA/Dec and the local sidereal time given the observation date and the location of MeerKAT, -30.7130S, 21.4430E. If this program is run for other observatories, the user must edit the source code in line 45 to obtain the `astropy.EarthLocation` of their observatory.

### Program Requirements
- Python >=3.0
- pandas
- astropy.Time
- astropy.EarthLocation
