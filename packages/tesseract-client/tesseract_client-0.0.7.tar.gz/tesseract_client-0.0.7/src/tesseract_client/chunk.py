from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class Chunk:
    file_path: str
    order: int
    hash: str

    @staticmethod
    def get_updated_chunks(
        old_chunks: list[Chunk],
        new_chunks: list[Chunk]
    ) -> list[tuple[Chunk, ChunkAction]]:
        updated_chunks = []
        if len(new_chunks) > len(old_chunks):
            # File has been appended to
            for chunk in new_chunks[len(old_chunks):]:
                updated_chunks.append((chunk, ChunkAction.CREATE))
        elif len(new_chunks) < len(old_chunks):
            # File has been truncated
            for chunk in old_chunks[len(new_chunks):]:
                updated_chunks.append((chunk, ChunkAction.DELETE))
        if len(old_chunks) > 0:
            for i, chunk in enumerate(new_chunks[:len(old_chunks)]):
                if chunk.hash != old_chunks[i].hash:
                    updated_chunks.append((chunk, ChunkAction.UPDATE))
        return updated_chunks


class ChunkAction(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
