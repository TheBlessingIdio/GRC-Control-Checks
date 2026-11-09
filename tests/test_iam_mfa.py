import boto3
from moto import mock_aws
from checks import iam_mfa

PASSWORD = "Str0ng!Passw0rd#1"


@mock_aws
def test_user_without_mfa_fails():
    iam = boto3.client("iam", region_name="us-east-1")
    iam.create_user(UserName="alice")
    iam.create_login_profile(UserName="alice", Password=PASSWORD)
    result = iam_mfa.run(iam)
    assert result["result"] == "FAIL"
    assert result["failing_resources"] == ["alice"]


@mock_aws
def test_user_with_mfa_passes():
    iam = boto3.client("iam", region_name="us-east-1")
    iam.create_user(UserName="bob")
    iam.create_login_profile(UserName="bob", Password=PASSWORD)
    device = iam.create_virtual_mfa_device(VirtualMFADeviceName="bob-device")
    serial = device["VirtualMFADevice"]["SerialNumber"]
    iam.enable_mfa_device(
        UserName="bob", SerialNumber=serial,
        AuthenticationCode1="123456", AuthenticationCode2="654321",
    )
    result = iam_mfa.run(iam)
    assert result["result"] == "PASS"