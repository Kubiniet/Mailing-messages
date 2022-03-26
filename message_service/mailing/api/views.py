import datetime

from celery.result import AsyncResult
from django.http import JsonResponse
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from message_service.mailing.models import Client, MailingList, Message
from message_service.mailing.tasks import send_messages_now_task

from .serializers import ClientSerializer, MailingListSerializer, MessageSerializer


class ClientsViewSet(viewsets.GenericViewSet):
    """Endpoint for the clients

    Args:
        viewsets (_type_): _description_

    Returns:
        _type_: Response, status_code
    """

    model = Client
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"])

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {"total": self.get_queryset().count(), "rows": data.data}
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Успешно зарегистрированный клиент!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response(
            {"message": "", "error": "Клиент не найден!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(
                instance=self.get_object().get(), data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Клиент успешно обновлен!"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response(
                {"message": "Клиент успешно удален!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Клиент не найден"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MailingViewSet(viewsets.GenericViewSet):
    """Endpoint for mailing

    Args:
        viewsets (_type_): get,post

    Returns:
         str: status message
         code: status code
    """

    model = MailingList
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"])

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {"total": self.get_queryset().count(), "rows": data.data}
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            mailing = MailingList.objects.last()
            mailing_id = mailing.id
            clients = Client.objects.filter(
                tag=mailing.clients["tag"], operator=mailing.clients["operator"]
            )
            if clients.exists():
                timezone = mailing.start_time.tzinfo
                now_in_timezone = datetime.datetime.now(timezone)
                count = 0
                for client in clients:
                    Message.objects.create(client=client, mailing=mailing)
                    count += 1
                if mailing.start_time <= now_in_timezone:
                    task = send_messages_now_task.delay(mailing_id)

                    return Response(
                        {
                            "message": "Рассылка успешно зарегистрирована!",
                            "count_message": count,
                            "status": AsyncResult(task.task_id).state,
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    schedule, created = ClockedSchedule.objects.get_or_create(
                        clocked_time=mailing.start_time
                    )
                    scheduled_task = PeriodicTask.objects.create(
                        clocked=schedule,
                        name="Рассылка {} в ожидонии до {}".format(
                            mailing.id, schedule.clocked_time
                        ),
                        task="message_service.mailing.tasks.send_messages_now_task",
                        args=JsonResponse([mailing_id], safe=False),
                        one_off=True,
                    )
                    return Response(
                        {
                            "message": "Рассылка успешно зарегистрирована и находится в ожидании!",
                            "scheduled_task": scheduled_task.name,
                        },
                        status=status.HTTP_201_CREATED,
                    )
            else:
                mailing.delete()
                return Response(
                    {
                        "message": "Ни один клиент не соответствует фильтру,рассылка не была создана",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response(
            {"message": "", "error": "Рассылка не найдена!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(
                instance=self.get_object().get(), data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Рассылка успешно обновлёна!"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response(
                {"message": "Рассылка успешно удалёна!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Рассылка не найдена!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A simple ViewSet for list the messages.
    """

    model = Message
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
