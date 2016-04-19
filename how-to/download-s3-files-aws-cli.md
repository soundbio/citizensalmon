### Downloading Data from S3
##### Via the AWS Command Line Interface (AWS CLI)

#### Setup
  1. [Download](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) the AWS CLI, if needed
  2. [Configure](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) the AWS CLI, if needed (talk to @zachmueller for the IAM credentials)
  3. [Documentation](http://docs.aws.amazon.com/cli/latest/reference/s3/) for the AWS CLI S3 tool

#### Download One File from S3

Example command to download one of the Larson (2014) raw data files from our S3 bucket:
```bash
aws s3 cp s3://citizensalmon/larson/raw-data/cjfas-2013-0502suppla.xlsx ./cjfas-2013-0502suppla.xlsx --region us-west-2
```

Breaking down each parameter:
  1. `aws` - The command itself
  2. `s3` - Tell the AWS CLI you want to interact with the S3 service
  3. `cp` - Use the s3 *"copy"* command
  4. `s3://citizensalmon/larson/raw-data/cjfas-2013-0502suppla.xlsx` - The *source* of the copy, in this case an S3 URI, composed of three main parts:
  	 - `s3://` denotes it is an S3 location
  	 - `citizensalmon/` is the bucket name
  	 - `larson/raw-data/cjfas-2013-0502suppla.xlsx` is the key of the object to be downloaded
  5. `./cjfas-2013-0502suppla.xlsx` - the *destination* for the file to be copied to, in this case a local location/file
  6. `--region us-west-2` - This option is not required, but may be necessary if the local AWS CLI profile's region does not match the region of the S3 bucket being referenced, i.e., `citizensalmon`

#### Download multiple files from S3

```bash
aws s3 cp s3://citizensalmon/larson/raw-data/ ./ --recursive
```

This is similar to downloading one file, with the following differences:
  1. Only a prefix is supplied, rather than a full key pointing to one object, i.e., `s3://citizensalmon/larson/raw-data/` points to a "folder" in the S3 bucket (also, the `./` is a local folder rather than a full filename, it can be a `/path/to/anywhere/`)
  2. The `--recursive` option tells the command to iterate through all objects that match the supplied prefix
  3. The `--region` parameter was left off in this example, but could be included, if necessary

**Note:** For all usage of the `cp` command, copying can be done between S3 buckets, as long as the profile used has the required access.

#### Upload to S3

```bash
aws s3 cp ./cjfas-2013-0502suppla.xlsx s3://citizensalmon/larson/raw-data/cjfas-2013-0502suppla.xlsx
```

Similar to downloading a file, simply swap the source and destination inputs to copy *from* the local drive *to* S3


#### List Objects in S3

Often it will be useful to look at the files that are in a given bucket. For example, to list all the raw data files from the Larson paper in our S3 bucket, the following command:
```bash
aws s3 ls s3://citizensalmon/larson/raw-data/
```

Yields:
```bash
2016-04-14 07:39:09      81357 cjfas-2013-0502suppla.xlsx
2016-04-14 07:39:09      79493 cjfas-2013-0502supplb.docx
2016-04-14 07:39:09      12252 cjfas-2013-0502supplc.xlsx
2016-04-14 07:39:10      12305 cjfas-2013-0502suppld.xlsx
2016-04-14 07:39:10      25643 cjfas-2013-0502supple.docx
2016-04-14 07:39:11       9156 cjfas-2013-0502supplf.xlsx
2016-04-14 07:39:15    2829761 cjfas-2013-0502suppli.fa
2016-04-14 07:38:53   14615158 genepop_western_alaska_chinook_RAD.txt
```

**Note:** There are limits around how many objects can be listed at once, refer to the full documentation for those additional details.
