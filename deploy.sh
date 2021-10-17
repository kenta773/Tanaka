#deploy command
if [ "$1" = "temp" ];then
    aws cloudformation deploy --template template.json --stack-name Tanaka-stack --parameter-overrides BucketName=tanakamenubucket FileName=menulist.csv DynamoDBTableName=TanakaMenuDB --capabilities CAPABILITY_NAMED_IAM
elif [ "$1" = "s3" ];then
    aws s3 sync s3 s3://tanakamenubucket/ --delete
else
    echo 'parameter error (temp or s3)'
fi