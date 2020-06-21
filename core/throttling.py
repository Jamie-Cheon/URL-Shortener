from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class VIPThrottle(UserRateThrottle):
    rate = '30/day'


class NormalThrottle(UserRateThrottle):
    rate = '10/day'


class AnonThrottle(AnonRateThrottle):
    rate = '3/day'

