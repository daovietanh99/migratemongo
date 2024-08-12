import pymongo
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import action
from bson.objectid import ObjectId
from datetime import datetime
from mongoapi.serializers import DocumentSerializer, MediaSerializer, ExperienceSerializer
from drf_spectacular.utils import extend_schema
from PIL import Image
import urllib
import io
import json
import boto3
import requests


class MongoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    
    source_string = settings.MONGO_SOURCE_URL
    target_string = settings.MONGO_TARGET_URL
    
    client_source = pymongo.MongoClient(source_string)
    client_target = pymongo.MongoClient(target_string)

    collection_source = client_source['iguide']["blogs"]
    collection_target = client_target['test']["blogs"]
    collection_experience_target = client_target['test']["experiences"]
    collection_media_target = client_target['test']["media"]
    
    session = boto3.Session()
    
    s3_client = session.client(
        service_name='s3',
        region_name=settings.S3_REGION,
        aws_access_key_id = settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key = settings.S3_SECRET_ACCESS_KEY,
        endpoint_url=settings.S3_ENDPOINT,
    )

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
    
    def _insert_image(self, url:str="", create=None, update=None, insert:bool=True, verbose:bool=False):
        urls = url.split('/')[-2:]
        name = '_'.join(urls).replace(' ', '-')
        
        upload_url = "https://iguide.z2p.dev/api/upload"

        payload = json.dumps({
            "sourcePath": urllib.parse.quote(url, safe=':/', encoding=None, errors=None),
            "name": name,
            "alt": name
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", upload_url, headers=headers, data=payload)
        
        data = response.json()
        
        img_serializer = MediaSerializer(data=data)
        img_serializer.is_valid(raise_exception=True)
        
        img_serializer.validated_data["createdAt"] = create
        img_serializer.validated_data["updatedAt"] = update
        if "thumbnailURL" in data:
            img_serializer.validated_data["thumbnailURL"] = data["thumbnailURL"]

        if verbose:
            print(payload, name, data, img_serializer.validated_data)

        return img_serializer.validated_data["id"]

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
        
        data.validated_data["meta"]["image"]["en"] = self._insert_image(data.validated_data["meta"]["image"]["en"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
        data.validated_data["meta"]["image"]["vi"] = self._insert_image(data.validated_data["meta"]["image"]["vi"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
        data.validated_data["meta"]["image"]["ko"] = self._insert_image(data.validated_data["meta"]["image"]["ko"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
                
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
    
    @action(methods=["POST"], detail=False, url_path="experience")
    def experience_create(self, request, *args, **kwargs):
        insert = True
        data = ExperienceSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        
        # data.validated_data["createdAt"]["$date"] = data.validated_data["createdAt"]["date"]
        # data.validated_data["updatedAt"]["$date"] = data.validated_data["updatedAt"]["date"]
        
        data.validated_data["createdAt"] = datetime.strptime(data.validated_data["createdAt"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        data.validated_data["updatedAt"] = datetime.strptime(data.validated_data["updatedAt"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")


        data.validated_data["banner"] = self._insert_image(data.validated_data["banner"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
        
        data.validated_data['highlight'] = json.loads(data.validated_data['highlight'])
        
        for blk in data.validated_data["blocks"]:
            if blk["blockType"] == "RichText":
                blk['content'] = json.loads(blk['content'])
            if blk["blockType"] == "OneOneLayout":
                blk['column1'] = json.loads(blk['column1'])
                blk['column2'] = json.loads(blk['column2'])
            elif blk["blockType"] == "Media":
                blk["media"] = self._insert_image(blk["media"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)
            elif blk["blockType"] == "Carousel":
                blk["carousel"] = json.loads(blk["carousel"])
                for img in blk["carousel"]:
                    img["media"] = self._insert_image(img["media"], data.validated_data["createdAt"], data.validated_data["updatedAt"], insert, True)

        data.validated_data['Content']['blocks'] = []
        data.validated_data['Content']['banner'] = data.validated_data["banner"]
                
        for blk in data.validated_data["blocks"]:
            if blk["blockType"] == "RichText":
                assert type(blk['content']) == dict
            elif blk["blockType"] == "Media":
                assert type(blk['media']) == str
            elif blk["blockType"] == "Carousel":
                assert type(blk['carousel']) == list             
        
        # print(data.validated_data)
        
        if self.collection_experience_target.find_one({"slug": data.validated_data["slug"]}):
            return Response(data={"message": "success", "result": {"data": data.validated_data}})
        
        if insert:
            instance = self.collection_experience_target.insert_one(data.validated_data)
            # data.validated_data["blocks"][1]["column2"]["en"]["root"]["children"][1]["fields"]["doc"] = instance.inserted_id
            # data.validated_data["blocks"][1]["column2"]["vi"]["root"]["children"][1]["fields"]["doc"] = instance.inserted_id
            # data.validated_data["blocks"][1]["column2"]["ko"]["root"]["children"][1]["fields"]["doc"] = instance.inserted_id
            
            self.collection_experience_target.update_one({
            '_id': instance.inserted_id
            },{
            '$set': {
                'blocks.1.column2.en.root.children.1.fields.doc': str(instance.inserted_id),
                'blocks.1.column2.vi.root.children.1.fields.doc': str(instance.inserted_id),
                'blocks.1.column2.ko.root.children.1.fields.doc': str(instance.inserted_id)
            }
            }, upsert=False)

        return Response(data={"message": "success", "result": {"data": request.data}})

