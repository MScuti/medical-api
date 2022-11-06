from rest_framework import serializers


class CommonCreateSerializer(serializers.Serializer):
    """ Common resource create serializer """
    pass


class CommonListSerializer(serializers.Serializer):
    """ Common resource list serializer """
    id = serializers.Field(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

class CommonDetailSerializer(serializers.Serializer):
    """ Common resource list serializer """
    id = serializers.Field(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")



class CommonUpdateSerializer(serializers.Serializer):
    """ Common resource update serializer """
    pass

