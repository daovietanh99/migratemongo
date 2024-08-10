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


class LocationSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    coordinates = serializers.ListSerializer(child=serializers.FloatField(), allow_empty=True, required=False)

class AtrributeSerializer(serializers.Serializer):
    difficulty = serializers.CharField(required=False)
    attributes = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    time = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    location = LocationSerializer(required=False)
    
class ContentSerializer(serializers.Serializer):
    title = MultilingualSerializer(required=False)
    description = MultilingualSerializer(required=False)
    blocks = RichTextBlockSerializer(required=False, many=True, allow_empty=True)      #modified
    banner = serializers.CharField(required=False)  
    
class SystemSerializer(serializers.Serializer):
    slug = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    path = serializers.CharField(required=False)

class ExperienceSerializer(serializers.Serializer):
    title = MultilingualSerializer(required=False)
    description = MultilingualSerializer(required=False)
    attributes = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    banner = serializers.CharField(required=False)                 #modified
    blocks = RichTextBlockSerializer(required=False, many=True, allow_empty=True)      #modified
    slug = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    difficulty = serializers.CharField(required=False)
    path = serializers.CharField(required=False)
    _status = serializers.CharField(required=False)
    time = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    location = LocationSerializer(required=False)
    createdAt = TimeSerializer(required=False) #modified
    updatedAt = TimeSerializer(required=False) #modified
    parent = serializers.CharField(required=False)
    meta = MetaSerializer(required=False)
    durationUnit = serializers.CharField(required=False)
    duration = serializers.IntegerField(required=False)
    address = serializers.CharField(required=False)
    seasons = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    accessibility = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    regions = serializers.CharField(required=False)
    highlight = serializers.CharField(required=False)
    # additionalInformation = serializers.CharField(required=False)
    Attribute = AtrributeSerializer(required=False)
    Content = ContentSerializer(required=False)
    System = SystemSerializer(required=False)