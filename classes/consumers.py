from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):   
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.name = self.scope['url_route']['kwargs']['name']
        # self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(self.name + " is Diconnected.")

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']
        action = data['action']
        message = data['message']
        if(action == "new-message"):
            await self.channel_layer.group_send(self.room_name,{
                'type':'chat.message',
                'message':message,
                'action' : 'new-message',
                'username':username
            })
        else:
            if(action == 'new-offer' or action == 'new-answer'):
                receiver_channel_name = data['message']['receiver_channel_name']
                data['message']['receiver_channel_name'] = self.channel_name
                await self.channel_layer.send(receiver_channel_name,{
                    'type':'send.sdp',
                    'data' : data
                })
            data['message']['receiver_channel_name'] = self.channel_name
            await self.channel_layer.group_send(self.room_name, {
                'type':'send.sdp',
                'data' : data
            })

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'username':username,
            'action' : 'new-message',
            'message':message
        })) 
    
    async def send_sdp(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))