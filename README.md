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

## Important Notes

## Program Requirements
