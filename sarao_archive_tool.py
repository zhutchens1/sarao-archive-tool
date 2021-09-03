"""
Tool for extracting summary data from "Details" tab of SARAO archive,
for LADUMA/MeerKAT tracks.

Zack Hutchens
March 2021
"""
from astropy.coordinates import EarthLocation
from astropy.time import Time

def time_string_to_decimals(time_string):
    fields = time_string.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    seconds = fields[2] if len(fields) > 2 else 0.0
    return float(hours) + (float(minutes) / 60.0) + (float(seconds) / pow(60.0, 2))


def extractinfo(detailsfile):
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
            #print(targetname)
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
        #if i==spectral_info_line and ("spectral_info_line" in locals()):
        #    print(line)
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
                startUTC = comp[0]
                startTime = Time(obsdate+' '+startUTC, scale='utc', location=meerkatloc)
                HAi = startTime.sidereal_time('apparent').value
                print(HAi)
                for revline in reversed(f.readlines()):
                    rcomp=revline.split()
                    if (("track" in rcomp[3]) and ("track" in rcomp[4]) and (targetname in rcomp[-1])) and ('HAf' not in locals()):
                        endUTC = rcomp[2]
                        endTime = Time(obsdate+' '+endUTC, scale='utc', location=meerkatloc)
                        HAf = endTime.sidereal_time('apparent').value
                        if HAf>HAi:
                            HArange = HAf-HAi
                        if HAf<HAi:
                            HArange = (HAf) + (24.-HAi)
                        print(HAi,HAf,HArange)


            #for line in reversed(f.readlines()):
            #    print('here')
            #    if (("track" in comp[3]) and ("track" in comp[4]) and (targetname in comp[-1])) and ('HAf' not in locals()):
            #        endUTC = comp[2]
            #        print("end UTC", endUTC)
            #        HAf=0.
        except: pass
            
    #return "Total On-Source Time: {a:0.3f} hrs = {b:0.3f} sec".format(a=onsourcetime, b=onsourcetime*3600)
    return season,track,obsdate,scheduleBlock,captureBlock,targetname,targetRA,targetDec,dumprate_Hz,datasize_GB,num_ants_used,missing_ants,onsourcetime,spwBand,spwProduct,spwCentreFreqMHz,\
            spwBandwidthMHz, spwChannels, spwChannelWidthkHz 
        

if __name__=='__main__':
    fname = input("Enter filename (e.g., input.txt): ")
    outstr = extractinfo(fname)
    print(outstr)
