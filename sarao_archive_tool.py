"""
Tool for extracting summary data from "Details" tab of SARAO archive,
for LADUMA/MeerKAT tracks.

Zack Hutchens
March 2021
"""
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
    for i, line in enumerate(f):
        comp = line.split()
        # get target name
        if "target" in line:
            targetname = comp[1]
            print(targetname)
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
                print(starttime, endtime, endtime-starttime)
        except: pass
    print("Total On-Source Time: {a:0.3f} hrs = {b:0.3f} sec".format(a=onsourcetime, b=onsourcetime*3600))
       
        

if __name__=='__main__':
    fname = input("Enter filename (e.g., input.txt): ")
    extractinfo(fname)
