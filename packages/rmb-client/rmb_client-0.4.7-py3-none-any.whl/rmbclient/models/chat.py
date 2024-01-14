from rmbcommon.models import ChatCore, BIAnswer
from rmbclient.models.base import convert_to_object, BaseResourceList
from rmbclient.models.run import RunList
from rmbclient.models.message import MessageList



class ChatClientModel(ChatCore):

    def delete(self):
        return self.api.send(endpoint=f"/chats/{self.id}", method="DELETE")

    @property
    def runs(self):
        return RunList(self.api, endpoint=f"/chats/{self.id}/runs")

    @property
    def messages(self):
        return MessageList(self.api, endpoint=f"/chats/{self.id}/messages")

    @convert_to_object(cls=BIAnswer)
    def ask(self, question):
        # 提问
        data = {"question": question}
        return self.api.send(endpoint=f"/chats/{self.id}", method="POST", data=data)


class ChatList(BaseResourceList):
    @convert_to_object(cls=ChatClientModel)
    def _get_all_resources(self):
        # 获取所有资源
        return self.api.send(endpoint=self.endpoint, method="GET")

    @convert_to_object(cls=ChatClientModel)
    def get(self, id):
        # 通过资源ID来获取
        return self.api.send(endpoint=f"{self.endpoint}{id}", method="GET")

    @convert_to_object(cls=ChatClientModel)
    def create(self, datasource_ids):
        data = {"datasource_ids": datasource_ids}
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)

