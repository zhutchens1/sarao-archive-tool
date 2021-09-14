"""
Tool for extracting summary data from "Details" tab of SARAO archive,
for LADUMA/MeerKAT tracks.

Zack Hutchens
March 2021
"""
from astropy.coordinates import EarthLocation
from astropy.time import Time
import os
import pandas as pd

def time_string_to_decimals(time_string):
    fields = time_string.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    seconds = fields[2] if len(fields) > 2 else 0.0
    return float(hours) + (float(minutes) / 60.0) + (float(seconds) / pow(60.0, 2))


def extractinfo(detailsfile):
    """
    Extract summary information from a plain-text LADUMA
    observing log.

    Parameters
    --------------
    detailsfile : str
        Path to the observing log, which should be in plain text format.
    
    Returns
    --------------
    infoarray : iterable
        Array containing extracted information from the log. The array
        follows the order and descriptions described in the README at 
        https://github.com/zhutchens1/sarao-archive-tool/.
    """
    try:
        f = open(detailsfile, 'r')
    except:
        raise IOError("cannot find specified file")

    # parse file
    onsourcetime = 0.0 # s
    meerkatloc=EarthLocation(lon=21+19/60+48/3600, lat=-30+49/60+48/3600)
    for i, line in enumerate(f):
        comp = line.split()
        # get target name
        if line.startswith("Name"):
            fields=line.split('/')
            captureBlock = fields[4]
        if "Experiment ID" in line:
            scheduleBlock = comp[-1]
        if "season" in line:
            season = comp[2]
        if "target" in line:
            targetname = comp[1]
        if "Observed from" in line:
            obsdate = comp[2]
        if "Description: " in line:
            track = comp[-1][:-1]
        if "Dump rate" in line:
            dumprate_Hz = comp[4]
        if "Size" in line:
            datasize_GB = comp[-2] 
        # get target RA/Dec
        if "target" in line:
            targetRA=comp[3]
            targetDec=comp[4]
        # get antenna info
        if "ants" in line:
            ants = line[8:-2].split()
            ants = [int(''.join(filter(str.isdigit, x))) for x in ants]
            num_ants_used = len(ants)
            missing = [x for x in range(0,64) if x not in ants]
            missing_ants = ''.join(['m'+str(x)+'-' for x in missing])[:-1]
        # get spectral window info
        if "Spectral" in line:
            spectral_info_line = i+2
        if "spectral_info_line" in locals():
            if i==spectral_info_line:
                spwBand = comp[1]
                spwProduct = comp[2]
                spwCentreFreqMHz = comp[3]
                spwBandwidthMHz = comp[4]
                spwChannels = comp[5]
                spwChannelWidthkHz = comp[6]
        # get on-source time
        try:
            if (("track" in comp[3]) and ("track" in comp[4]) and (targetname in comp[-1])):
                starttime=time_string_to_decimals(comp[0]) # decimal hrs
                endtime=time_string_to_decimals(comp[2]) # decimal hrs
                rawdelta = endtime-starttime
                if rawdelta>=0.0:
                    onsourcetime+=rawdelta
                else:
                    onsourcetime += ((24.-starttime)+(endtime)) # if observation crosses midnight
        except: pass

        # get range of hour angles
        try:
            if (("track" in comp[3]) and ("track" in comp[4]) and (targetname in comp[-1])) and ('HAi' not in locals()):
                targetRAdecimals=time_string_to_decimals(targetRA)
                startUTC = comp[0]
                startTime = Time(obsdate+' '+startUTC, scale='utc', location=meerkatloc)
                HAi = startTime.sidereal_time('apparent').value
                HAi = HAi - targetRAdecimals
                for revline in reversed(f.readlines()):
                    rcomp=revline.split()
                    if rcomp==[]: continue
                    #if (("track" in rcomp[3]) and ("track" in rcomp[4]) and (targetname in rcomp[-1])) and ('HAf' not in locals()):
                    if revline.count("track")==2 and (targetname in rcomp[-1]) and ('HAf' not in locals()):
                        endUTC = rcomp[2][-8:]
                        endTime = Time(obsdate+' '+endUTC, scale='utc', location=meerkatloc)
                        HAf = endTime.sidereal_time('apparent').value
                        HAf = HAf - targetRAdecimals
        except: pass
    print("Processing "+detailsfile)        
    infoarray = [season,track,obsdate,scheduleBlock,captureBlock,targetname,targetRA,targetDec,dumprate_Hz,datasize_GB,num_ants_used,\
            missing_ants,onsourcetime,HAi,HAf,spwBand,spwProduct,spwCentreFreqMHz,spwBandwidthMHz, spwChannels, spwChannelWidthkHz]
    return infoarray 

def create_table(path_to_logs):
    """
    Create a summary table from a directory
    of LADUMA observing logs.

    Parameters
    -----------------
    path_to_logs : str
        Path to the directory which contains the plain-text format LADUMA logs.
i       The directory should not contain other files.

    Returns    
    ----------------
    df : pandas.DataFrame object
        pandas DataFrame containing summary information from all observing logs.
    """
    files = os.listdir(path_to_logs)
    table=[]
    for f in files:
        table.append(extractinfo(path_to_logs+f))
    df = pd.DataFrame(table,columns=['season','track','obsdate','scheduleBlock','captureBlock','targetname','targetRA','targetDec',\
            'dumprate_Hz','datasize_GB','num_ants_used','missing_ants','onsourcetime','ihourangle','fhourangle','spwBand','spwProduct',\
            'spwCentreFreqMHz', 'spwBandwidthMHz', 'spwChannels', 'spwChannelWidthkHz'])
    return df 


if __name__=='__main__':
    logpath = input("Enter directory where logs are stored: ")
    table = create_table(logpath)
    savename = input("Enter name where summary table should be saved as CSV: ")
    table.to_csv(savename,index=False)
