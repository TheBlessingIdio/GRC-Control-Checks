import boto3
from checks.common import build_result


def run(iam=None):
    iam = iam or boto3.client("iam")
    users = []
    for page in iam.get_paginator("list_users").paginate():
        users.extend(page["Users"])

    failing = []
    for user in users:
        name = user["UserName"]
        # Only users who can sign in to the console need MFA
        try:
            iam.get_login_profile(UserName=name)
        except iam.exceptions.NoSuchEntityException:
            continue
        if not iam.list_mfa_devices(UserName=name)["MFADevices"]:
            failing.append(name)

    return build_result(
        "IAM-MFA", not failing, len(users), failing,
        {"users_checked": [u["UserName"] for u in users]},
    )