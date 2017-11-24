from rest_framework import serializers
from .models import *
from rest_framework import pagination


class BayStateAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BayStateAuction
        fields = ('id', 'status', 'date', 'time', 'address', 'city', 'zipcode',
                  'state', 'deposit', 'message', 'message_avail')


class TownAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TownAuction
        fields = ('id', 'status', 'date', 'time', 'address', 'city', 'zipcode', 'country',
                  'state', 'deposit', 'message', 'message_avail')


class LandMarkAuctionSerliazer(serializers.ModelSerializer):
    class Meta:
        model = LandMarkAuction
        fields = ('id', 'status', 'date', 'time', 'address', 'city', 'zipcode', 'country',
                  'state', 'deposit', 'message', 'message_avail')

class CommonWealthAuctionSerliazer(serializers.ModelSerializer):
    class Meta:
        model = CommonWealthAuction
        fields = ('id', 'status', 'date', 'time', 'address', 'city', 'zipcode', 'country',
                  'state', 'deposit', 'message', 'message_avail')


class TimelineSerializer(serializers.Serializer):
    baystateauction = BayStateAuctionSerializer(many=True)
    townauction = TownAuctionSerializer(many=True)


class PaginatedTimelineSerializer(pagination.DjangoPaginator):
    class Meta:
        object_serializer_class = TimelineSerializer
