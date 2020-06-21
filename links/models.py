from django.db import models
from users.models import User
from hashlib import md5
import time
import string
from random import randint

base_list = string.ascii_letters + string.digits


def encoder(num):
    result = []
    while num:
        result.append(base_list[num % 62])
        num //= 62

    return "".join(reversed(result))


class Link(models.Model):
    origin_url = models.URLField("Url", help_text='Your shortened URL will be computed')
    short_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    owner = models.ForeignKey(User, related_name='links', on_delete=models.CASCADE, blank=True, null=True)

    def __repr__(self):
        return f'origin url: {self.origin_url} short url: {self.short_url}'

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            millis = int(round(time.time() * 1000))
            encoded_url = md5(self.origin_url.encode()).hexdigest()[:10]
            url_Num = 0
            ran_num = 0

            # generate encoded url to integers
            for i in encoded_url:
                url_Num += ord(i)

            # generate random integers
            for _ in range(100):
                ran_num = randint(0, 100)

            self.short_url = encoder(millis) + encoder(url_Num) + encoder(ran_num)
        return super().save(*args, **kwargs)
