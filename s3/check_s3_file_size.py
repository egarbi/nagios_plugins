#!/usr/bin/env python

##########################################################
#
# Written by Matthew McMillan
# matthew.mcmillan@gmail.com
# @matthewmcmillan
# https://matthewcmcmillan.blogspot.com
# https://github.com/matt448/nagios-checks
#
# Modified by quique@enriquegarbi.com.ar
# https://github.com/egarbi/nagios_plugins/tree/master/s3
#
# -- Nagios error codes --
#    0 = OK/green
#    1 = WARNING/yellow
#    2 = CRITICAL/red
#    3 = UNKNOWN/purple

import botocore
import boto3
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='This script is a Nagios check that \
                                              monitors the size of a list of files in \
                                              an S3 bucket.')

parser.add_argument('--profile', dest='profile', type=str, required=False, default='default',
                    help='AWS profile to use to connect')

parser.add_argument('--bucketname', dest='bucketname', type=str, required=True,
                    help='Name of S3 bucket')

parser.add_argument('--proxyhost', dest='proxyhost', type=str, default='',
                    help='Proxy to establish a connection trough (optional).')

parser.add_argument('--warning', dest='warning', type=int, default=0,
                    help='The Warning threshold in bytes for size \
                          Default is 0 (It will never fail) \
                          ')

parser.add_argument('--critical', dest='critical', type=int, default=0,
                    help='The Critical threshold in bytes for size \
                          Default is 0 (It will never fail).')

parser.add_argument('--files', dest='files', type=str, required=True,
                    help='List of files to be checked within the bucketname (ie: ["path/to/one/file","path/to/another/file"])')

parser.add_argument('--debug', action='store_true',
                    help='Enables debug output.')

args = parser.parse_args()

# Assign variables from command line arguments
bucketname = args.bucketname
proxyhost = args.proxyhost
warning = args.warning
critical = args.critical
files = args.files.split(",")
criticallist = []
warninglist = []

if (args.debug):
    print '########## START DEBUG OUTPUT ############'
    print 'DEBUG: S3 BUCKET NAME: ' + str(bucketname)

if (args.debug):
    print "DEBUG: Connecting to S3"

session = boto3.session.Session(profile_name=args.profile)
if (args.proxyhost):
  s3 = session.resource('s3',config=Config(proxies={'http': proxyhost, 'https': proxyhost}))
else:
  s3 = session.resource('s3')

if (args.debug):
    print "DEBUG: S3 Connection: %s" % s3

# Check if bucket exists. Exit with critical if it doesn't
bucket = s3.Bucket(bucketname)
exists = True

try:
    s3.meta.client.head_bucket(Bucket=bucketname)
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

if exists is False:
    print "CRITICAL: No bucket found with a name of " + str(bucketname)
    exit(2)
else:
    if (args.debug):
        print "DEBUG: Hooray the bucket " + str(bucketname) + " was found!"

if (args.debug):
    print "Bucket: %s" % bucket

if (args.debug):
    print 'WARNING Size Thresholds: {0} bytes'.format(warning)

if (args.debug):
    print 'CRITICAL Size Thresholds: {0} bytes'.format(critical)

for file in files:
    object = s3.Object(bucketname,file)
    size = object.content_length
    if (args.debug):
      print ' Size of {0} is {1} bytes'.format(file,size)
    if size < critical:
        criticallist.append(file)
    elif size > critical and size < warning:
        warninglist.append(file)

lengthCritical = len(criticallist)
lengthWarning = len(warninglist)
if lengthCritical > 0 and lengthWarning > 0:
    print 'CRITICAL: There are {0} files in critical status: {1} and {2} in warning status: {3} '.format(lengthCritical, criticallist, lengthWarning, warninglist)
    exitcode = 2
elif lengthCritical > 0 and lengthWarning == 0:
    print 'CRITICAL: There are {0} files in critical status: {1}'.format(lengthCritical, criticallist)
    exitcode = 2
elif lengthCritical == 0 and lengthWarning > 0:
    print 'WARNING: There are {0} files: in warning status: {1}'.format(lengthWarning, warninglist)
    exitcode = 1
else:
    print 'OK: All files are within the size boundaries'
    exitcode = 0

exit(exitcode)
