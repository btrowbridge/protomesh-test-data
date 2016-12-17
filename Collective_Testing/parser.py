from matplotlib import pyplot as plt
import re
import os

class NodeResults:
    def __init__(self, filename):
        # Some usefull regex
        resultPattern = r"^([\d\.]+)\s+:.+max =.+/(\d+)/"
        self.resultMatcher = re.compile(resultPattern, re.MULTILINE)

        # Latency to all other nodes
        self.nodeLatencies = {}
        self.meanLatency = None

        # Load
        self.load(filename)


    def load(self, filename):
        # Read in all the text from filename
        f=open(filename, 'r')
        text=f.read()
        f.close()

        # Record data
        totalLatency = 0
        for match in self.resultMatcher.finditer(text):
            nodeID = match.group(1)
            latency = int( match.group(2) )
            self.nodeLatencies[nodeID] = latency
            totalLatency += latency

        # If there was no data gathered, throw an exception
        if len( self.nodeLatencies ) == 0:
            raise Exception('No data found in "{}"'.format(filename))
        self.meanLatency = totalLatency / len(self.nodeLatencies)


class IntervalTest:
    def __init__(self, rootPath, interval):
        self.rootPath = rootPath
        self.interval = interval

        # Generate full path
        if not rootPath[-1]=='/':
            rootPath += '/'
        self.path = rootPath + str(interval) + '/'

        # Results from individual nodes and their average
        self.nodeList = []
        self.meanLatency = None

        # Load
        self.load( self.path )

    def load(self, path):
        # Open all node result files
        totalLatency = 0
        for filename in os.listdir(self.path):
            if 'result' in filename:
                try:
                    result = NodeResults(path+filename)
                except Exception as e:
                    print('Exception encountered reading node results from file "{}". \n{}\nSkipping...'.format(path+filename, str(e)))
                    continue
                self.nodeList.append( result )

                totalLatency += result.meanLatency

        # Calculate average latency
        self.meanLatency = totalLatency / len(self.nodeList)


def graphTest(testPath, ax=None):
    if testPath[-1] != '/':
        title = testPath
        testPath += '/'
    else:
        title = testPath[:-1]

    # Find valid "interval" sub-directories
    intervals = []
    for dirName in os.listdir(testPath):
        try:
             intervals.append( int(dirName) )
        except Exception:
            continue

    # Find the mean latencies for each ping interval
    intervals.sort()
    meanLatencies = []
    for interval in intervals:
        test = IntervalTest(testPath, interval)
        meanLatencies.append( test.meanLatency )

    # Plot it
    if ax != None:
        plt.axes(ax)
    plt.title(title)
    plt.xlabel('Ping Interval (ms)')
    plt.ylabel('Aggragate Mean Latency (ms)')
    plt.ylim([0,2500])
    plt.plot(intervals, meanLatencies, marker='o')

if __name__ == '__main__':
    f, (ax1, ax2, ax3) = plt.subplots(1,3)
    graphTest('128_bytes', ax1)
    graphTest('1472_bytes', ax2)
    graphTest('1500_bytes', ax3)
    plt.show()
