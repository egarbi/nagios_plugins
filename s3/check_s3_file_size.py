#!/usr/bin/env python

import datetime
from datetime import timedelta, tzinfo
import botocore
import boto3
import argparse
import re

# Parse command line arguments
parser = argparse.ArgumentParser(description='This script is a Nagios check that \
                                              monitors the age of files that have \
                                              been backed up to an S3 bucket.')

parser.add_argument('--profile', dest='profile', type=str, required=False, default='default',
                    help='AWS profile to use to connect')

parser.add_argument('--bucketname', dest='bucketname', type=str, required=True,
                    help='Name of S3 bucket')

parser.add_argument('--bucketfolder', dest='bucketfolder', type=str, default='',
                    help='Folder to check inside bucket (optional).')

parser.add_argument('--debug', action='store_true',
                    help='Enables debug output.')

args = parser.parse_args()

# Assign variables from command line arguments
bucketname = args.bucketname
bucketfolder = args.bucketfolder
bucketfolder_regex = '^' + bucketfolder

filecount = 0

if (args.debug):
    print '########## START DEBUG OUTPUT ############'
    print 'DEBUG: S3 BUCKET NAME: ' + str(bucketname)


if (args.debug):
    print "DEBUG: Connecting to S3"

session = boto3.session.Session(profile_name=args.profile)
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

# Loop through keys (files) in the S3 bucket and
# check each one for min and max file age.
for key in bucket.objects.filter(Prefix=bucketfolder):
        if key.size == 0:
            filecount += 1

msg = 'There is/are %s empty file/s in this bucket: ' % str(filecount)
if filecount > 0:

    statusline = 'CRITICAL: ' + msg
    exitcode = 2
elif filecount == 0:
    statusline = 'OK: ' + msg
    exitcode = 0
else:
    statusline = 'UNKNOWN: ' + msg
    exitcode = 3

print statusline
exit(exitcode)
