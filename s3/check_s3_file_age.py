#!/usr/bin/env python

##########################################################
#
# Written by Matthew McMillan
# matthew.mcmillan@gmail.com
# @matthewmcmillan
# https://matthewcmcmillan.blogspot.com
# https://github.com/matt448/nagios-checks
#
#
# This Nagios check looks at the age of files stored in an S3 bucket.
# It alerts if files haven't been uploaded within a certain time frame
# and/or alerts if files are too old.
# This script requires authentication credentials to be stored in
# the config file '~/.boto'.
#
#
# .boto file format:
#
#   [Credentials]
#       aws_access_key_id = ABCDEFJKJK39939
#       aws_secret_access_key = 443xkdjksjkldsjfklsdjsdkjsdfkls32xkj2333
#
#
#
# -- Nagios error codes --
#    0 = OK/green
#    1 = WARNING/yellow
#    2 = CRITICAL/red
#    3 = UNKNOWN/purple
#

import datetime
from datetime import timedelta, tzinfo
import botocore
import boto3
import argparse
import re


# A UTC class.
ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


# Parse command line arguments
parser = argparse.ArgumentParser(description='This script is a Nagios check that \
                                              monitors the age of files that have \
                                              been backed up to an S3 bucket.')

parser.add_argument('--profile', dest='profile', type=str, required=False, default='default',
                    help='AWS profile to use to connect')

parser.add_argument('--bucketname', dest='bucketname', type=str, required=True,
                    help='Name of S3 bucket')

parser.add_argument('--proxyhost', dest='proxyhost', type=str, default='',
                    help='Proxy to establish a connection trough (optional).')

parser.add_argument('--warning', dest='warning', type=int, default=0,
                    help='The age of the file in hours to generate a warning notification \
                          Default is 0 hours (disabled).\
                          ')

parser.add_argument('--critical', dest='critical', type=int, default=0,
                    help='The age of the file in hours to generate a critical notification \
                          Default is 0 hours (disabled).')

parser.add_argument('--files', dest='files', type=str, required=True,
                    help='List of files to be checked within the bucketname (ie: ["path/to/one/file","path/to/another/file"])')
####
# Add arg option for s3 region?
###
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
    print 'DEBUG: WARNING THRESHOLD: ' + str(warning)
    print 'DEBUG: CRITICAL THRESHOLD: ' + str(critical)


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

# Figure out time delta between current time and warning/critical thresholds
warningagetime = datetime.datetime.now(
    UTC()) - datetime.timedelta(hours=warning)
if (args.debug):
    print 'WARNING AGE TIME: ' + str(warningagetime)

criticalagetime = datetime.datetime.now(
    UTC()) - datetime.timedelta(hours=critical)
if (args.debug):
    print 'CRITICAL AGE TIME: ' + str(criticalagetime)

for file in files:
    object = s3.Object(bucketname,file)
    last_modified = object.last_modified
    if (args.debug):
      print ' Age of {0}: {1}'.format(file,last_modified)
    if last_modified < criticalagetime:
        criticallist.append(file)
    elif last_modified > criticalagetime and last_modified < warningagetime:
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
    print 'OK: All files are within the time boundaries'
    exitcode = 0

exit(exitcode)
