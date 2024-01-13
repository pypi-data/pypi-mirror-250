import os

from pebbleauthclient.constants import JWKS_EXP_TIME
from pebbleauthclient import auth

token = "eyJ0eXAiOiJhdCtqd3QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjBfdl8ycWFYTFFrb1NIYjBRX0d5Ulp1OFZ1X2llVTVHT1UtN0JhUFY4M0UifQ.eyJhdWQiOlsiYXBpLnBlYmJsZS5zb2x1dGlvbnMvdjUvcHJvamVjdCIsImFwaS5wZWJibGUuc29sdXRpb25zL3Y1L2FjdGlvbiJdLCJleHAiOjE3MzY2MDQ0NzYsImlhdCI6MTcwNDk4MzcwMywiaXNzIjoiTWFjQm9vay1Qcm8tZGUtR3VpbGxhdW1lLmxvY2FsIiwibHYiOjUsInJvbGVzIjpbIm1hbmFnZXIiXSwic2NvcGUiOiJwcm9qZWN0OnJlYWQgcHJvamVjdDpjcmVhdGUgcHJvamVjdDp3cml0ZS5vd24gYWN0aW9uOnJlYWQgYWN0aW9uOndyaXRlLmFzc2lnbmVkIGFjdGlvbjpjcmVhdGUgcHJvamVjdDpkZWxldGUiLCJzdWIiOiJ0ZXN0QHBlYmJsZS5iemgiLCJ0aWQiOiIxamUzNGstZWQ0NWRzc3EtZWsiLCJjbGllbnRfaWQiOiIwMUhLUTVHUkdHU1I3U0ZCQjFCTTRTUkY4NSIsImp0aSI6Ijg4ZDVlOTcwLWI4YTMtNDJjYy05ZjFmLWQzZTU1NzFjYjBlZiJ9.hyXgK8dUXtCzkgM-rat9FQd-TODh3dro0Vi694XA5pgo0JxO6Yea5WrCwigTqDGhQySB95bgzrQ7uBJMcnqevYQsSXZE1FMgMagOxMaZk5-JpaqHGXxt27zFvq7m4RzNOxLg75GPTCDwL7aY6Azxku4AAuSiReGy9GNrDX9rutPdUdgp3_886_29MsRLt1T5yxOYxfOUi1oe_9-QW_o7_r92t1zZsTrwBb3Gelo5Ox8p53gJgiSLROZUi6fpXTGts4zuzdg2J70b0jmxCSAM87xoOiI3NCm9Cb9kqC0isCUFvm_f2nhiW8nOcvqqtbX76wAo4QWWNACjeJc-DAX3OA"

"""
while True:
    print("Input a valid JWT token (type Q to exit) : ")
    token = input()

    if token.lower() == "q":
        break"""

auth_token = auth(token, options={
    'audience': "api.pebble.solutions/v5/action"
})
user = auth_token.get_user()
licence = auth_token.get_authenticated_licence()

print(JWKS_EXP_TIME)
print(os.getenv('PBL_JWKS_LAST_UPDATE'))

print(auth_token)
print(user)
print(licence)

print(user.has_scopes(['project:list', 'project:read']))
