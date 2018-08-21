### Checking empty files
```
./check_s3_file_size.py  --profile testingnagios --bucketname "somebucket"
CRITICAL: There is/are 1 empty file/s in this bucket
```
### Checking min age of files in a bucket
```
./check_s3_file_age.py --profile testingnagios --bucketname "somebucket" --minfileage 10000000
OK: S3 files meet MIN time boundaries. - MIN:10000000hrs - Files meeting MIN time: 1 - Total file count: 1
```
