from rest_framework import serializers

class MultilingualSerializer(serializers.Serializer):
    en = serializers.CharField(required=False)
    vi = serializers.CharField(required=False)
    ko = serializers.CharField(required=False)

class RichTextBlockSerializer(serializers.Serializer):
    content = serializers.CharField(required=False) #modified
    carousel = serializers.CharField(required=False) #modified
    media = serializers.CharField(required=False)    #modified
    blockType = serializers.CharField(required=False)
    autoplay = serializers.BooleanField(required=False)
    autoplaySpeed = serializers.IntegerField(required=False)
    ratio = serializers.CharField(required=False)
    isFullWidth = serializers.BooleanField(required=False)
    
class MetaSerializer(serializers.Serializer):
    title =  MultilingualSerializer(required=False)
    description = MultilingualSerializer(required=False)
    image = MultilingualSerializer(required=False)
    # isApproveText = serializers.BooleanField(required=False)
    # isFinalCheckOnWeb = serializers.BooleanField(required=False)
    # deploy = serializers.BooleanField(required=False)
    # isHighlight = serializers.BooleanField(required=False)
    # isApproveImage = serializers.BooleanField(required=False)
    
class TimeSerializer(serializers.Serializer):
    date = serializers.CharField(required=False)
    
class MediaSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    alt = serializers.CharField(required=False)
    prefix = serializers.CharField(required=False, default="dev/media")
    filename = serializers.CharField(required=False)
    mimeType =  serializers.CharField(required=False, default="image/jpeg")
    filesize = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    focalX = serializers.IntegerField(required=False)
    focalY = serializers.IntegerField(required=False)
    url = serializers.CharField(required=False)

class DocumentSerializer(serializers.Serializer):
    title = MultilingualSerializer(required=False)
    description = MultilingualSerializer(required=False)
    banner = serializers.CharField(required=False)                 #modified
    blocks = RichTextBlockSerializer(required=False, many=True, allow_empty=True)      #modified
    slug = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    path = serializers.CharField(required=False)
    _status = serializers.CharField(required=False)
    createdAt = TimeSerializer(required=False) #modified
    updatedAt = TimeSerializer(required=False) #modified
    _v = serializers.IntegerField(required=False, default=0)
    parent = serializers.CharField(required=False)
    meta = MetaSerializer(required=False)
