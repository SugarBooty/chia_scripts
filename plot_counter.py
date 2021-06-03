import subprocess

remoteHost = 'bert@192.168.1.26'
datesList = []
lsDir = '/mnt/hdd*/*'
datesDict = {}

# formats the file name of a plot and returns only the date string
def format_data(name):
    # splits the path given by /
    splitByPath = name.split('/')
    # selects the last element of the list ( the file name ) and removes everything but the date string
    dateInName = (splitByPath[-1])[9:19]
    #returns the date string
    return dateInName

# runs the ls command and returns a list of date strings from the plot files found
def retrieve_dates(command) :
    # saves the output of the ls command to the var 'result'
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # decodes the byte string into a regular one and splits it on newline
    resultSplitByLine = (result[0].decode('utf-8')).split("\n")
    # runs 'format_data' on each element of the list individually and saves the result to another list
    resultDateStr = *map(format_data, resultSplitByLine),
    # returns the final formated date string
    return resultDateStr

# returns a list of date strings for all the plots on the systems
# prints how many local, remote, and plots there are in total
def get_list_of_plots() :
    # the remote command to run that will retrieve all the plot paths
    remoteCommand = f"ssh {remoteHost} 'ls {lsDir}'"
    # the local command to run that will retrieve all the plot paths
    localCommand = f"ls {lsDir}"

    # retrieves the local date strings
    localResultList = retrieve_dates(localCommand)
    #retrieves the remote date strings
    remoteResultList = retrieve_dates(remoteCommand)
    # combines the lists together
    resultList = localResultList + remoteResultList

    print(f'Local plots: {len(localResultList)} \nRemote plots: {len(remoteResultList)} \nTotal plots:  {len(resultList)}')

    # returns the full file list
    return (resultList)

# itterates through the list of date strings and counts how many of each duplicate there are
for date in get_list_of_plots():
    # if the key (date) is not already in the dict, set its value (occurence number) to 0
    datesDict.setdefault(date, 0)
    # add one to the value of the key (date)
    datesDict[date] += 1

# sort the dict by key (date) and print it in order
for date in sorted(datesDict.keys()):
    print(f'{date}: {datesDict[date]} Plots!')
