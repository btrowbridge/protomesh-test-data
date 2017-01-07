from matplotlib import pyplot as plt
import re
import os

class NodeResults:
    def __init__(self, filename):
        # Some usefull regex
        resultPattern = r"^([\d\.]+)\s+:.+loss = .+/(\d+)%.+max =.+/(\d+)/"
        self.resultMatcher = re.compile(resultPattern, re.MULTILINE)

        # Latency and drop rates to all other nodes
        self.latencies = {}
        self.dropRates = {}
        self.meanLatency = None
        self.meanDropRate = None

        # Load
        self.load(filename)


    def load(self, filename):
        # Read in all the text from filename
        f=open(filename, 'r')
        text=f.read()
        f.close()

        # Record data
        totalLatency = 0
        totalDropRate = 0
        self.latencies = {}
        self.dropRates = {}
        for match in self.resultMatcher.finditer(text):
            nodeID = match.group(1)
            dropRate = int( match.group(2) )
            latency = int( match.group(3) )
            self.latencies[nodeID] = latency
            self.dropRates[nodeID] = dropRate
            totalLatency += latency
            totalDropRate += dropRate

        # If there was no data gathered, throw an exception
        if len( self.latencies ) == 0:
            raise Exception('No data found in "{}"'.format(filename))
        self.meanLatency = totalLatency / len(self.latencies)
        self.meanDropRate = totalDropRate / len(self.dropRates)


class IntervalTest:
    def __init__(self, rootPath, interval):
        self.rootPath = rootPath
        self.interval = interval

        # Generate full path
        if not rootPath[-1]=='/':
            rootPath += '/'
        self.path = rootPath + str(interval) + '/'
        print(self.path)

        # Results from individual nodes and their average
        self.nodeList = []
        self.meanLatency = None
        self.meanDropRate = None

        # Load
        self.load( self.path )

    def load(self, path):
        # Open all node result files
        totalLatency = 0
        totalDropRate = 0
        for filename in os.listdir(self.path):
            if 'result' in filename:
                try:
                    result = NodeResults(path+filename)
                except Exception as e:
                    print('Exception encountered reading node results from file "{}". \n{}\nSkipping...'.format(path+filename, str(e)))
                    continue
                self.nodeList.append( result )

                totalLatency += result.meanLatency
                totalDropRate += result.meanDropRate

        # Calculate average latency
        self.meanLatency = totalLatency / len(self.nodeList)
        self.meanDropRate = totalDropRate / len(self.nodeList)


def graphTestLatency(testPath, ax=None, ymax=2500, title=None):
    # Determine graph title
    if title == None:
        if testPath[-1] != '/':
            title = testPath
            testPath += '/'
        else:
            title = testPath[:-1]
        slashInd=title.rfind('/')
        title = title[slashInd+1:]

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
    plt.ylim([0, ymax])
    plt.plot(intervals, meanLatencies, marker='o')

def graphTestDropRate(testPath, ax=None, ymax=100, title=None):
    # Determine graph title
    if title == None:
        if testPath[-1] != '/':
            title = testPath
            testPath += '/'
        else:
            title = testPath[:-1]
        slashInd=title.rfind('/')
        title = title[slashInd+1:]

    # Find valid "interval" sub-directories
    intervals = []
    for dirName in os.listdir(testPath):
        try:
             intervals.append( int(dirName) )
        except Exception:
            continue

    # Find the mean latencies for each ping interval
    intervals.sort()
    meanDropRates = []
    for interval in intervals:
        test = IntervalTest(testPath, interval)
        meanDropRates.append( test.meanDropRate )

    # Plot it
    if ax != None:
        plt.axes(ax)
    plt.title(title)
    plt.xlabel('Ping Interval (ms)')
    plt.ylabel('Aggragate Mean Drop Rate (%)')
    plt.ylim([0, ymax])
    plt.plot(intervals, meanDropRates, marker='o')


def graphLatencyRun1():
    f, (ax1, ax2, ax3) = plt.subplots(1,3)
    graphTestLatency('one-channel/ping-tests/128_bytes', ax1)
    graphTestLatency('one-channel/ping-tests/1472_bytes', ax2)
    graphTestLatency('one-channel/ping-tests/1500_bytes', ax3)
    plt.show()

def graphLatencyRun2():
    graphTestLatency('two-channel/ping-tests/128_bytes', ymax=500)
    plt.show()

def graphDropRateRun1():
    f, (ax1, ax2, ax3) = plt.subplots(1,3)
    graphTestDropRate('one-channel/ping-tests/128_bytes', ax=ax1)
    graphTestDropRate('one-channel/ping-tests/1472_bytes', ax=ax2)
    graphTestDropRate('one-channel/ping-tests/1500_bytes', ax=ax3)
    plt.show()

def graphDropRateRun2():
    graphTestDropRate('two-channel/ping-tests/128_bytes', ymax=5)
    plt.show()



def graphSummary():
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    # Single Channel
    graphTestLatency('one-channel/ping-tests/128_bytes', title='Single-Channel Latency', ax=ax1)
    graphTestDropRate('one-channel/ping-tests/128_bytes', title='Single-Channel Drop Rate', ax=ax3)

    # Multi Channel
    graphTestLatency('two-channel/ping-tests/128_bytes', title='Multi-Channel Latency', ax=ax2)
    graphTestDropRate('two-channel/ping-tests/128_bytes', title='Multi-Channel Drop Rate', ax=ax4)

if __name__ == '__main__':
    graphSummary()
    plt.show()
