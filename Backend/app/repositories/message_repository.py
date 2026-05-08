from pymongo.asynchronous.cursor import AsyncCursor
from pymongo.results import InsertOneResult
from pymongo.asynchronous.collection import AsyncCollection
from datetime import datetime, timezone
from bson import ObjectId, objectid
from Backend.app.core.database import get_database
from Backend.app.models import Message, Role
from typing import cast


class MessageRepository:

    COLLECTION_NAME: str = "messages"

    async def create(
        self,
        conversation_id: str,
        role: Role,
        content: str,
    ) -> Message:

        now: datetime = datetime.now(tz=timezone.utc)
        document: dict[str, object] = {
            "conversation_id": objectid.ObjectId(oid=conversation_id),
            "role": role,
            "content": content,
            "created_at": now,
        }

        collection: AsyncCollection[dict[str, object]] = get_database(
        ).get_collection(name=self.COLLECTION_NAME)
        result: InsertOneResult = await collection.insert_one(document=document)
        return Message(
            id=str(cast(object, result.inserted_id)),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=now,
        )

    async def list_by_conversation(self, conversation_id: str) -> list[Message]:
        collection: AsyncCollection[dict[str, object]] = get_database(
        ).get_collection(name=self.COLLECTION_NAME)
        cursor: AsyncCursor[dict[str, object]] = collection.find(
            filter={
                "conversation_id": ObjectId(oid=conversation_id)
            }
        ).sort(key_or_list="created_ad", direction=1)

        messages: list[Message] = []
        async for document in cursor:
            messages.append(
                Message(
                    id=str(document["_id"]),
                    conversation_id=str(document["conversation_id"]),
                    role=cast(Role, document["role"]),
                    content=cast(str, document["content"]),
                    created_at=cast(datetime, document["created_at"]),
                ))
        return messages
