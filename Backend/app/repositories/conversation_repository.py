from datetime import datetime, timezone
from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult
from typing import cast

from app.core.database import get_database
from app.models import Conversation
from app.repositories.message_repository import MessageRepository


class ConversationRepository:

    COLLECTION_NAME: str = "conversations"

    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository: MessageRepository = message_repository

    async def create(self, title: str) -> Conversation:
        now: datetime = datetime.now(tz=timezone.utc)
        document: dict[str, object] = {
            "title": title,
            "created_at": now,
            "updated_at": now,
        }

        collection: AsyncCollection[dict[str, object]] = get_database().get_collection(
            name=self.COLLECTION_NAME
        )
        result: InsertOneResult = await collection.insert_one(document=document)

        return Conversation(
            id=str(cast(object, result.inserted_id)),
            title=title,
            created_at=now,
            updated_at=now,
        )

    async def find_by_id(self, conversation_id: str) -> Conversation | None:
        collection: AsyncCollection[dict[str, object]] = get_database().get_collection(
            name=self.COLLECTION_NAME
        )
        document: dict[str, object] | None = await collection.find_one(
            filter={"_id": ObjectId(conversation_id)}
        )

        if document is None:
            return None

        return Conversation(
            id=str(document["_id"]),
            title=cast(str, document["title"]),
            created_at=cast(datetime, document["created_at"]),
            updated_at=cast(datetime, document["updated_at"]),
        )

    async def list_all(self) -> list[Conversation]:
        collection: AsyncCollection[dict[str, object]] = get_database().get_collection(
            name=self.COLLECTION_NAME
        )
        cursor: AsyncCursor[dict[str, object]] = collection.find().sort(
            key_or_list="updated_at", direction=-1
        )

        conversations: list[Conversation] = []
        async for document in cursor:
            conversations.append(
                Conversation(
                    id=str(document["_id"]),
                    title=cast(str, document["title"]),
                    created_at=cast(datetime, document["created_at"]),
                    updated_at=cast(datetime, document["updated_at"]),
                )
            )
        return conversations

    async def touch_updated(self, conversation_id: str) -> None:
        now: datetime = datetime.now(tz=timezone.utc)
        collection: AsyncCollection[dict[str, object]] = get_database().get_collection(
            name=self.COLLECTION_NAME
        )
        _: UpdateResult = await collection.update_one(
            filter={"_id": ObjectId(conversation_id)},
            update={"$set": {"updated_at": now}},
        )

    async def delete(self, conversation_id: str) -> bool:
        
        _ = await self._message_repository.delete_by_conversation(
            conversation_id=conversation_id
        )

        collection: AsyncCollection[dict[str, object]] = get_database().get_collection(
            name=self.COLLECTION_NAME
        )
        result: DeleteResult = await collection.delete_one(
            filter={"_id": ObjectId(conversation_id)}
        )
        return result.deleted_count == 1