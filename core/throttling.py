from rest_framework.throttling import UserRateThrottle


class VIPThrottle(UserRateThrottle):
    rate = '20/day'


class NormalThrottle(UserRateThrottle):
    rate = '5/day'


