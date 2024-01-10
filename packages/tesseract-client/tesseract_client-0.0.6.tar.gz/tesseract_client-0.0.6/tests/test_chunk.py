from tesseract_client.chunk import Chunk, ChunkAction


def test_get_updated_chunks():
    indexed_chunks = [
        Chunk(
            file_path="test.txt",
            order=1,
            hash="hash1"
        ),
        Chunk(
            file_path="test.txt",
            order=2,
            hash="hash2"
        ),
        Chunk(
            file_path="test.txt",
            order=3,
            hash="hash3"
        )
    ]
    chunks = indexed_chunks
    updated_chunks = Chunk.get_updated_chunks(indexed_chunks, chunks)
    assert len(updated_chunks) == 0

    chunks = [
        Chunk(
            file_path="test.txt",
            order=1,
            hash="hash1"
        ),
        Chunk(
            file_path="test.txt",
            order=2,
            hash="hash2"
        ),
        Chunk(
            file_path="test.txt",
            order=3,
            hash="hash4"
        )
    ]
    updated_chunks = Chunk.get_updated_chunks(indexed_chunks, chunks)
    assert len(updated_chunks) == 1
    assert updated_chunks[0][0].order == 3
    assert updated_chunks[0][1] == ChunkAction.UPDATE

    chunks = [
        Chunk(
            file_path="test.txt",
            order=1,
            hash="hash1"
        ),
        Chunk(
            file_path="test.txt",
            order=2,
            hash="hash4"
        ),
        Chunk(
            file_path="test.txt",
            order=3,
            hash="hash3"
        )
    ]
    updated_chunks = Chunk.get_updated_chunks(indexed_chunks, chunks)
    assert len(updated_chunks) == 1
    assert updated_chunks[0][0].order == 2
    assert updated_chunks[0][1] == ChunkAction.UPDATE

    chunks = [
        Chunk(
            file_path="test.txt",
            order=1,
            hash="hash2"
        ),
        Chunk(
            file_path="test.txt",
            order=2,
            hash="hash3"
        ),
    ]
    updated_chunks = Chunk.get_updated_chunks(indexed_chunks, chunks)
    assert len(updated_chunks) == 3
    assert updated_chunks[0][0].order == 3
    assert updated_chunks[0][1] == ChunkAction.DELETE
    assert updated_chunks[1][0].order == 1
    assert updated_chunks[1][1] == ChunkAction.UPDATE
    assert updated_chunks[2][0].order == 2
    assert updated_chunks[2][1] == ChunkAction.UPDATE
