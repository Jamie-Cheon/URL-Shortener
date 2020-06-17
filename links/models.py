from django.db import models
from django.contrib.auth.models import User
from hashlib import md5

base_list = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
base = len(base_list)


class Link(models.Model):
    origin_url = models.URLField("Url", help_text='Your shortened URL will be computed')
    short_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')

    def __repr__(self):
        return f'origin url: {self.origin_url}'

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.short_url = md5(self.origin_url.encode()).hexdigest()[:10]

        return super().save(*args, **kwargs)










    # def save(self, *args, **kwargs):
    #     print(self.id, self.origin_url)
    #     if self.short_url == '':
    #         self.short_url = self.get_short_id
    #         print('this is shortened url:', self.short_url)
    #     super(Url, self).save(*args, **kwargs)
    #
    # @property
    # def get_short_id(self):
    #     print('this is self.id: ', self.id)
    #     res = self.encode_id(self.id)
    #     return res
    #
    # def encode_id(self, num):
    #     print('This is encode_id func')
    #     print('num: ', num)
    #     result = []
    #     while num:
    #         result.append(base_list[num % base])
    #         num //= base
    #
    #     return "".join(reversed(result))



    # @staticmethod
    # def decode_id(code: str):
    #     num = 0
    #     code_list = list(code)
    #     for index, code in enumerate(reversed(code_list)):
    #         num += base_list.index(code) * base ** index
    #     return num

