import datetime

import requests
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from config import celery_app
from config.settings.base import TOKEN_JWT

from .models import Client, MailingList, Message


@celery_app.task()
def send_messages_now_task(mailing_id):
    """
    Task take mailind id and send a request.Post to the external API

    Args:
        mailing_id (int): _description_

    Returns:
        str: status
    """
    try:
        mailing = MailingList.objects.get(id=mailing_id)
        clients = Client.objects.filter(
            tag=mailing.clients["tag"], operator=mailing.clients["operator"]
        )
        auth_token = TOKEN_JWT
        headers = {
            "Authorization": "Bearer " + auth_token,
            "Content-Type": "application/json",
        }
        for client in clients:
            message = get_object_or_404(Message, mailing=mailing, client=client)
            payload = JsonResponse(
                {
                    "id": message.id,
                    "phone": int(client.phone_number[1:]),
                    "text": "mailing.text",
                }
            )

            url = "https://probe.fbrq.cloud/v1/send/{}".format(message.id)
            r = requests.request("POST", url, headers=headers, data=payload, timeout=10)

            message.sending_status = True
            message.save()
            r.raise_for_status()

        mailing.end_time = datetime.datetime.now(mailing.start_time.tzinfo)
        mailing.save()

        return "Сообщения отправлены клиентам"

    except requests.exceptions.RequestException as err:
        return f"Ошибка: Что пошло не так {err}"
    except requests.exceptions.HTTPError as errh:
        return f"Http Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Ошибка соединения: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except Http404:
        return f"Рассылка {mailing_id} не найдена "
