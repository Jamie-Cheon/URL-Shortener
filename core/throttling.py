from rest_framework.throttling import UserRateThrottle


class VIPThrottle(UserRateThrottle):
    rate = '5/minute'


class NormalThrottle(UserRateThrottle):
    rate = '1/minute'

