from django.db import models


class KcDonateRecord(models.Model):
    donator = models.CharField('捐款人', max_length=20)
    donate_time = models.DateTimeField('捐款时间')
    amount = models.DecimalField('捐款金额', max_digits=8, decimal_places=2)
    note = models.CharField('捐款人留言', max_length=200)

    class Meta:
        verbose_name = '捐款记录'
        verbose_name_plural = '捐款记录'

    def __str__(self):
        return '%s捐款%.2f元' % (self.donator, self.amount)