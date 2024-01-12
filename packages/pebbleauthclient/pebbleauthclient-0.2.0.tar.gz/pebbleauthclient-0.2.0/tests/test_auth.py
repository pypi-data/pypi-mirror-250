import os

from pebbleauthclient.constants import JWKS_EXP_TIME
from pebbleauthclient import auth

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBfdl8ycWFYTFFrb1NIYjBRX0d5Ulp1OFZ1X2llVTVHT1UtN0JhUFY4M0UiLCJ0eXAiOiJhdCtqd3QifQ.eyJzdWIiOiJ0ZXN0QHBlYmJsZS5iemgiLCJpc3MiOiJNYWNCb29rLVByby1kZS1HdWlsbGF1bWUubG9jYWwiLCJhdWQiOlsiYXBpLnBlYmJsZS5zb2x1dGlvbnMvdjUvcHJvamVjdCIsImFwaS5wZWJibGUuc29sdXRpb25zL3Y1L2FjdGlvbiJdLCJ0aWQiOiIxamUzNGstZWQ0NWRzc3EtZWsiLCJyb2xlcyI6WyJtYW5hZ2VyIl0sImx2Ijo1LCJjbGllbnRfaWQiOiIwMUhLUTVHUkdHU1I3U0ZCQjFCTTRTUkY4NSIsInNjb3BlIjoicHJvamVjdDpyZWFkIHByb2plY3Q6Y3JlYXRlIHByb2plY3Q6d3JpdGUub3duIGFjdGlvbjpyZWFkIGFjdGlvbjp3cml0ZS5hc3NpZ25lZCBhY3Rpb246Y3JlYXRlIHByb2plY3Q6ZGVsZXRlIiwiaWF0IjoxNzA0OTc1NDY0LCJleHAiOjE3MDQ5NzkwNjQsImp0aSI6IjFhNmZhNmExLTEzNWYtNDZkNS05NWYxLWJiODU4ZGM4Y2NmNiJ9.PUmdu82PjcqTG1lN-TgtfWfaoKX8JzhOfrpODiaveH1rzS8KJbZf6wHGgwf491nO0lqUnM745WboUHPj48DsHYb3dpzmy5Es1oolAJ1uJjmz1L62Ma1KvfCTnWB1j6tPBABTMa2-J-tIWuU5qbo7R1KJItvN1xiIzOCJauLqmxaT5ZNjacXcjhQH0CidIc_L60tDBU3rBNb4zLI7pJJ2_z7TYEUJkKS7mD2gh90wsjot0FYs3nwtnzJH17-7xL-BFcVwKmAb8z6CwnZufTW9pRRRPJTgI9_Jh4oJpgczOTbgneniZHnYBvbND-q9u9iaEOivG0n8a0k6K8ppNg-zvA"

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

print(user.has_scopes(['project:write.own']))
