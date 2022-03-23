from rest_framework import serializers

from message_service.mailing.models import Client, MailingList, Message


class FilterClientSerializer(serializers.Serializer):
    tag = serializers.CharField()
    operator = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MailingListSerializer(serializers.ModelSerializer):
    clients = FilterClientSerializer()

    class Meta:
        model = MailingList
        fields = "__all__"
