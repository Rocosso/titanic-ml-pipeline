
This workflow work only if IAM is set:

```JSON Policy into IAM
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "sagemaker:*",
        "ecr:*",
        "cloudformation:*",
        "iam:*"
      ],
      "Resource": "*"
    }
  ]
}
```


OIDC must be configured in AWS IAM:
```
aws iam create-role --role-name GitHubActionsRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_ORG/REPO:ref:refs/heads/main"
        }
      }
    }]
  }'
```

Set the secrets for IAM

AWS_ACCOUNT
AWS_REGION
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
MODEL_NAME
