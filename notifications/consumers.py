from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.response import Response
import json
from .service import asyncBlogCreation,notification_room
from organization.service import async_get_organization
from follow.service import async_organization_following,async_user_following
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

class organization(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            print('connected')
            self.user=self.scope['user']
            if not self.user.is_authenticated:
                await self.close()
                return 
            await self.accept()
            try:
                self.group_user=f'user_{self.user.id}'
                organization=await async_get_organization(self)
                self.group_organization=f'organization_{organization.Name}'
                self.notification_organization_group=f'notification_{organization.Name}'
                self.user_followings=await async_user_following(self)
                self.organization_followings= await async_organization_following(self)

                self.followings=set(self.user_followings + self.organization_followings)
                await self.channel_layer.group_add(self.group_organization,self.channel_name)
                await self.channel_layer.group_add(self.notification_organization_group,self.channel_name)
                await self.channel_layer.group_add(self.group_user,self.channel_name)
                if self.followings:
                    for following in self.followings:
                        notification=f'notification_{following}'
                        await self.channel_layer.group_add(notification,self.channel_name)
            except Exception:
                await self.close()
                
        
        except Exception as e:
            logger.exception('could not connect to websocket.')
            await self.close()

            

    async def disconnect(self, code):
        if hasattr(self, "group_organization"):
            await self.channel_layer.group_discard(
                self.group_organization,
                self.channel_name
            )

        if hasattr(self, "notification_organization_group"):
            await self.channel_layer.group_discard(
                self.notification_organization_group,
                self.channel_name
            )

        if hasattr(self, "group_user"):
            await self.channel_layer.group_discard(
                self.group_user,
                self.channel_name
        )
    

    
    async def receive(self, text_data = None, bytes_data = None):
        return await super().receive(text_data, bytes_data)
    

    async def blog_notification(self,event):
        try:
            await asyncBlogCreation(self,event)

            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception('blog notification could not be sent.')



    async def follower_employee(self,event):

        room=f'notification_{event["name"]}'
        await self.channel_layer.group_add(room,self.channel_name)
        

    async def follower_employee_to_founder(self,event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception :
            logger.exception('could not send follow notification to founder.')


    async def follower_founder(self,event):

        room=notification_room(event["name"])
        await self.channel_layer.group_add(room,self.channel_name)
    

    async def unfollower_employee(self,event):

        room=notification_room(event["name"])
        await self.channel_layer.group_discard(room,self.channel_name)
        

    async def comments(self,event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception('comment could not be sent through websocket')


    async def comments_update(self,event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception('updated comment could not be sent through websocket')
        
        


    async def comments_delete(self,event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception('deleted comment could not be sent through websocket')


    async def unfollower_founder(self,event):

        room=notification_room(event["name"])
        await self.channel_layer.group_discard(room,self.channel_name)
    
        


    async def unfollower_employee_to_founder(self,event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception('could not send the unfollow notification to founder.')











        
