### Checking empty files
```
> ./check_s3_file_size.py  --profile testing \
--bucketname "somebucket" 

CRITICAL: There is/are 1 empty file/s in this bucket
```
if you are behind a proxy:
```
> ./check_s3_file_size.py  --profile testing \
--proxyhost "127.0.0.1:3128" \
--bucketname "somebucket"

CRITICAL: There is/are 1 empty file/s in this bucket
```
### Checking age of files in a bucket
```
> ./check_s3_file_age.py --profile testing \
--bucketname "acloudgurupresigned1" \
--warning 390 \
--critical 400 \
--files "hello.txt,vacio.txt"

CRITICAL: There are 1 files in critical status: ['hello.txt']
```
if you are behind a proxy:
```
> ./check_s3_file_age.py --profile testing \
--bucketname "acloudgurupresigned1" \
--warning 390 \
--critical 400 \
--files "hello.txt,vacio.txt" \
--proxyhost "127.0.0.1:3128"

CRITICAL: There are 1 files in critical status: ['hello.txt']
```

