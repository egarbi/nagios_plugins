### Checking size of files in a bucket
```
> ./check_s3_file_size.py  --profile testing \
--bucketname "somebucket" \
--warning 15 \
--critical 18 \
--files "hello.txt,vacio.txt"

CRITICAL: There are 1 files in critical status: ['vacio.txt']
```
if you are behind a proxy:
```
> ./check_s3_file_size.py  --profile testing \
--proxyhost "127.0.0.1:3128" \
--bucketname "somebucket" \
--warning 15 \
--critical 18 \
--files "hello.txt,vacio.txt"

CRITICAL: There are 1 files in critical status: ['vacio.txt']
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

