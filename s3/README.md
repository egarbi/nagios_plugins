### Checking empty files
```
./check_s3_file_size.py  --profile testingnagios --bucketname "somebucket"
CRITICAL: There is/are 1 empty file/s in this bucket
```
if you are behind a proxy:
```
./check_s3_file_size.py  --profile testingnagios --proxyhost "127.0.0.1:3128" --bucketname "somebucket"
CRITICAL: There is/are 1 empty file/s in this bucket
```
### Checking min age of files in a bucket
```
./check_s3_file_age_modified.py --debug --profile testing --bucketname "acloudgurupresigned1" --warning 390 --critical 400 --files "hello.txt,vacio.txt"
CRITICAL: There are 1 files in critical status: ['hello.txt']
```

