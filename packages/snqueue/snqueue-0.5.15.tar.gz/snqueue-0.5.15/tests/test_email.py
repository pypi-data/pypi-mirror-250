import os
from snqueue.boto3_clients.kms_client import KmsClient
from snqueue.boto3_clients.s3_client import S3Client
from snqueue.utils.email import get_s3_email

profile_name = 'terminus'

# Getting email from S3
bucket_name = 'incoming-mail-littledumb'
#object_key = '6gmu0p32jlfa0et6t1fsvc9hvcdaqp6tnthv3jo1'
object_key = '3n5usjpr3jmkjnliipcq3j21cq3j2qov9lbsbuo1'

with S3Client(profile_name) as s3:
  with KmsClient(profile_name) as kms:
    with get_s3_email(s3, kms, bucket_name, object_key) as email:
      print(email)
      if len(email.Attachments) > 0:
        print(os.stat(email.Attachments[0]))

