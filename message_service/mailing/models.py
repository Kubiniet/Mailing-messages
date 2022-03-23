from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from message_service.mailing.choices import TIMEZONES


class Client(models.Model):

    phone_regex = RegexValidator(
        regex=r"^\+?7?\d{7,10}$",
        message="Phone number must be entered in the format: '+799999999'. Up to 10 digits not allowed.",
    )

    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        validators=[phone_regex],
        max_length=10,
        blank=True,
    )
    operator = models.IntegerField(
        verbose_name=_("Operator code"),
        validators=[MaxValueValidator(999), MinValueValidator(900)],
    )
    tag = models.CharField(verbose_name=_("Tag"), max_length=50)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return " Клиент {} с тегом {} ".format(self.pk, self.tag)


class MailingList(models.Model):

    clients = models.JSONField(_("Filter for Client List"), null=False)
    start_time = models.DateTimeField(
        _("Start time"), auto_now=False, auto_now_add=False
    )
    end_time = models.DateTimeField(
        _("Send Time"), auto_now=False, auto_now_add=False, null=True, blank=True
    )
    text = models.CharField(_("Message Text"), max_length=250)

    class Meta:
        verbose_name = _("Mailing List")
        verbose_name_plural = _("Mailing Lists")

    def __str__(self):
        return " Рассылка {} выпусщена  {} ".format(self.pk, self.start_time)


class Message(models.Model):

    client = models.ForeignKey(
        "Client", verbose_name=_("Client"), on_delete=models.CASCADE
    )
    mailing = models.ForeignKey(
        "MailingList", verbose_name=_("Mailing List"), on_delete=models.CASCADE
    )
    sending_status = models.BooleanField(_("Status"), default=False)
    start_date = models.DateTimeField(verbose_name=_("Start Date"), auto_now=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return "Сообщение id {} на телефон {} ".format(
            self.pk, self.client.phone_number
        )
