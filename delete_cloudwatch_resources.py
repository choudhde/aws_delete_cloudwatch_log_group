__author__ = 'dc'
####
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
####

import boto3
import sys
import argparse
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import math

aws_region = 'ca-central-1'
s3_bucket = 'bucket-name-lambda-s3'
s3_prefix = 'exported-logs'
num_days = 1
log_group_name = ['/aws/lambda/lambda-function-watcher-prod-lambdaWatcher']


######################################
#
#######################################
def publish_logs_s3(log_client):

    try:

        logDate = datetime.now() - timedelta(days=num_days)
        print (logDate)
        startOfDay = logDate.replace(hour=0, minute=0, second=0, microsecond=0)
        print(startOfDay)
        endOfDay = logDate.replace(hour=23, minute=59, second=59, microsecond=999999)
        print(endOfDay)

        for log in log_group_name:
            response = log_client.create_export_task(
             taskName='export_task',
             logGroupName=log,
             fromTime=math.floor(startOfDay.timestamp() * 1000),
             to=math.floor(endOfDay.timestamp() * 1000),
             destination=s3_bucket,
             destinationPrefix=s3_prefix
            )

    except ClientError as err:
        print("Error: {}".format(err))

####################
# Main Function Call
####################
def main():

    # Take arguments from user
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help="AWS profile name to use to run this command")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()

    session = boto3.session.Session(
        profile_name=args.profile
    )
    print(session)
    # Initializing Client
    log_client = boto3.client('logs', region_name=aws_region)
    """ :type: pyboto3.iam """

    # Calling the function to delete all cloudwatch logs & alarms
    publish_logs_s3(log_client)


# If ran on the CLI, go ahead and run it
if __name__ == "__main__":
    main()