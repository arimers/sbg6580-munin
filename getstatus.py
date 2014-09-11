#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import sys
import urllib2
#from scrapy.contrib.loader import ItemLoader

def parseContent6500(content):
  result = {'upstreamChannels': [], 'downstreamChannels': []}
  soup = BeautifulSoup(content)
  downstream = soup.find(text='Downstream Bonded Channels')
  downstreamtable = downstream.findParent('table')
  channelrows = downstreamtable.findAll('tr')
  for row in channelrows:
    cols = row.findAll('td')
    if len(cols) == 1:
      continue
    assert(len(cols) == 9)
    num = cols[0].contents[0]
    if num == 'Channel':
      continue
    chan = {}
    chan['number'] = num
    chan['lockStatus'] = cols[1].contents[0]
    chan['modulation'] = cols[2].contents[0]
    chan['id'] = cols[3].contents[0]
    chan['frequency'] = cols[4].contents[0]
    chan['power'] = cols[5].contents[0]
    chan['snr'] = cols[6].contents[0]
    chan['correctables'] = cols[7].contents[0]
    chan['uncorrectables'] = cols[8].contents[0]
    result['downstreamChannels'].append(chan)

  upstream = soup.find(text='Upstream Bonded Channels')
  upstreamtable = upstream.findParent('table')
  #print repr(upstreamtable)
#  assert(len(upstream) == 1)
  channelrows = upstreamtable.findAll('tr')
  #print repr(channelrows)
  for row in channelrows:
    cols = row.findAll('td')
    if len(cols) == 1:
      continue
    #print repr(cols)
    assert(len(cols) == 7)
    num = cols[0].contents[0]
    if num == "Channel":
      continue
    #print repr(num)
    chan = {}
    chan['number'] = num
    chan['lockStatus'] = cols[1].contents[0]
    chan['type'] = cols[2].contents[0]
    chan['id'] = cols[3].contents[0]
    chan['symbolrate'] = cols[4].contents[0]
    chan['frequency'] = cols[5].contents[0]
    chan['power'] = cols[6].contents[0]
    result['upstreamChannels'].append(chan)
  return result

def muninProcess(info):
  if len(sys.argv) > 1 and sys.argv[1] == "config":
    print 'multigraph downstreamsnr'
    print 'graph_title Downstream Channel SNR'
    print 'graph_vlabel dB'
    print 'graph_category cable'
    print 'graph_info This graph shows Downstream Channel SNR'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downsnr{num}.label Channel {num}'.format(num=chanNum)
    print 'multigraph downstreampower'
    print 'graph_title Downstream Channel Power'
    print 'graph_vlabel dBmV'
    print 'graph_category cable'
    print 'graph_info This graph shows Downstream Channel Power'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downpower{num}.label Channel {num}'.format(num=chanNum)
    print 'multigraph downstreamcorrectables'
    print 'graph_title Downstream Channel Errors, Correctable'
    print 'graph_vlabel correctables / min'
    print 'graph_category cable'
    print 'graph_info This graph shows Downstream Channel Correctables'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downcorr{num}.label Channel {num}'.format(num=chanNum)
      print 'downcorr{num}.type COUNTER'.format(num=chanNum)
      print 'downcorr{num}.graph_period minute'.format(num=chanNum)
    print 'multigraph downstreamuncorrectables'
    print 'graph_title Downstream Channel Errors, Uncorrectable'
    print 'graph_vlabel uncorrectables / min'
    print 'graph_category cable'
    print 'graph_info This graph shows Downstream Channel Uncorrectables'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downuncorr{num}.label Channel {num}'.format(num=chanNum)
      print 'downuncorr{num}.type COUNTER'.format(num=chanNum)
      print 'downuncorr{num}.graph_period minute'.format(num=chanNum)
    print 'multigraph upstreampower'
    print 'graph_title Upstream Channel Power'
    print 'graph_vlabel dBmV'
    print 'graph_category cable'
    print 'graph_info This graph shows Upstream Channel Power'
    for channel in info['upstreamChannels']:
      chanNum = channel['number']
      print 'uppower{num}.label Channel {num}'.format(num=chanNum)
  else:
    print 'multigraph downstreamsnr'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      power = channel['snr'].replace(' dB','').replace(' ','')
      if power == '0.0':
        power = 'u' # unknown. 0.0 might actually be an ok value, but it makes min hard to read
      print 'downsnr{num}.value {value}'.format(num=chanNum, value=power)
    print 'multigraph downstreampower'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      power = channel['power'].replace(' dBmV','').replace(' ','')
      if power == '0.0':
        power = 'u' # unknown. 0.0 might actually be an ok value, but it makes min hard to read
      print 'downpower{num}.value {value}'.format(num=chanNum, value=power)
    print 'multigraph downstreamcorrectables'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downcorr{num}.value {value}'.format(num=chanNum, value=channel['correctables'])
    print 'multigraph downstreamuncorrectables'
    for channel in info['downstreamChannels']:
      chanNum = channel['number']
      print 'downuncorr{num}.value {value}'.format(num=chanNum, value=channel['uncorrectables'])
    print 'multigraph upstreampower'
    for channel in info['upstreamChannels']:
      chanNum = channel['number']
      power = channel['power'].replace(' dBmV','').replace(' ','')
      if power == '0.0':
        power = 'u' # unknown. 0.0 might actually be an ok value, but it makes min hard to read
      print 'uppower{num}.value {value}'.format(num=chanNum, value=power)

def testSample():
  with open ("sampledata.html", "r") as myfile:
    data=myfile.read()
  connectionInfo = parseContent6500(data)
  #print repr(connectionInfo)
  muninProcess(connectionInfo)

def getAndProcess():
  data = urllib2.urlopen('http://192.168.0.1/RgConnect.asp', timeout=30).read()
  connectionInfo = parseContent6500(data)
  muninProcess(connectionInfo)


#testSample()
getAndProcess()
