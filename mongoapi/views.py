import pymongo
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import action
from bson.objectid import ObjectId
from datetime import datetime
from mongoapi.serializers import DocumentSerializer, MediaSerializer
from drf_spectacular.utils import extend_schema
from PIL import Image
import urllib
import io
import json


class MongoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    
    source_string = 'mongodb://iguide:iguide_123456@54.254.236.140/iguide' 
    target_string = 'mongodb+srv://admin:Y3sLjnTUjv@cms-dev.8prvnv1.mongodb.net/test?retryWrites=true&w=majority&appName=cms-dev'
    
    client_source = pymongo.MongoClient(source_string)
    client_target = pymongo.MongoClient(target_string)

    collection_source = client_source['iguide']["blogs"]
    collection_target = client_target['test']["blogs"]
    collection_media_target = client_target['test']["media"]

    def list(self, request, *args, **kwargs):
        ids = self.collection_source.count_documents(filter={})
        # cursor = self.collection_source.find({})
        # ids = []
        # for document in cursor:
        #     ids.append(str(document["_id"]))
        return Response(data={"message": "success", "result": {"ids": ids}})

    def retrieve(self, request, pk):
        document = self.collection_source.find_one(ObjectId(pk))
        document["_id"] = str(document["_id"])
        return Response(data={"message": "success", "result": {"data": document}})
    
    def _insert_image(self, url, create, update, insert:bool=True, verbose:bool=False):
        image_obj = self.collection_media_target.find_one({"filename": url.split("/")[-1]})
        
        if image_obj:
            return str(image_obj["_id"])
        
        fd = urllib.request.urlopen( urllib.parse.quote(url, safe=':/', encoding=None, errors=None) )
        image_file = io.BytesIO(fd.read())
        img = Image.open(image_file)
        img_serializer = MediaSerializer(data={
            "mimeType": "image/" + img.format.lower(),
            "filename": url.split("/")[-1],
            "filesize": image_file.tell(),
            "width": img.size[0],
            "height": img.size[1],
            "createdAt": create,
            "updatedAt": update
        })
        img_serializer.is_valid(raise_exception=True)
        if verbose:
            print(img_serializer.validated_data)
        img_obj = "Test"
        if insert:
            img_obj = str(self.collection_media_target.insert_one(img_serializer.validated_data).inserted_id)
        return img_obj

    @extend_schema(request=DocumentSerializer)
    def create(self, request, *args, **kwargs):
        insert = True
        data = DocumentSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        
        # data.validated_data["createdAt"]["$date"] = data.validated_data["createdAt"]["date"]
        # data.validated_data["updatedAt"]["$date"] = data.validated_data["updatedAt"]["date"]
        
        data.validated_data["createdAt"] = datetime.strptime(data.validated_data["createdAt"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        data.validated_data["updatedAt"] = datetime.strptime(data.validated_data["updatedAt"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")


        data.validated_data["banner"] = self._insert_image(data.validated_data["banner"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
        
        for blk in data.validated_data["blocks"]:
            if blk["blockType"] == "RichText":
                blk['content'] = json.loads(blk['content'])
            elif blk["blockType"] == "Media":
                blk["media"] = self._insert_image(blk["media"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
            elif blk["blockType"] == "Carousel":
                blk["carousel"] = json.loads(blk["carousel"])
                for img in blk["carousel"]:
                    img["media"] = self._insert_image(img["media"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
                
        for blk in data.validated_data["blocks"]:
            if blk["blockType"] == "RichText":
                assert type(blk['content']) == dict
            elif blk["blockType"] == "Media":
                assert type(blk['media']) == str
            elif blk["blockType"] == "Carousel":
                assert type(blk['carousel']) == list             
        
        # print(data.validated_data)
        
        if self.collection_target.find_one({"slug": data.validated_data["slug"]}):
            return Response(data={"message": "success", "result": {"data": data.validated_data}})
        
        if insert:
            self.collection_target.insert_one(data.validated_data)

        return Response(data={"message": "success", "result": {"data": request.data}})

