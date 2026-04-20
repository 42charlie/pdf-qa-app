from config import CHUNK_SIZE, OVERLAP_SIZE, MIN_CHUNK_SIZE

def split_large_block(block: str, max_size: int) -> list:
    """
    Split a single large block into smaller pieces using:
    sentence → space → hard cut fallback
    """
    chunks = []
    start = 0
    length = len(block)

    while start < length:
        end = start + max_size

        if end >= length:
            chunks.append(block[start:].strip())
            break

        # Try to split at sentence boundary
        split_pos = block.rfind(".", start, end)
        if split_pos == -1:
            split_pos = block.rfind(" ", start, end)

        # Fallback: hard cut
        if split_pos == -1 or split_pos <= start:
            split_pos = end

        chunks.append(block[start:split_pos].strip())
        start = split_pos

    return [c for c in chunks if c]


def chunk_text(text: str):
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]

    chunks = []
    cursor = 0  # tracks position in full_text
    current_chunk = ""
    chunk_start = 0

    for block in blocks:
        block_start = text.find(block, cursor)  # find exact position
        if block_start == -1:
            continue

        cursor = block_start

        # handle large block
        if len(block) > CHUNK_SIZE:
            sub_blocks = split_large_block(block, CHUNK_SIZE)
        else:
            sub_blocks = [block]

        for sub_block in sub_blocks:
            sub_start = text.find(sub_block, cursor)
            if sub_start == -1:
                continue

            sub_end = sub_start + len(sub_block)

            if len(current_chunk) + len(sub_block) + 2 <= CHUNK_SIZE:
                if not current_chunk:
                    chunk_start = sub_start

                current_chunk += sub_block + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append({
                        "content": current_chunk.strip(),
                        "start_char": chunk_start,
                        "end_char": prev_end
                    })

                # overlap
                if chunks:
                    overlap_text = chunks[-1]["content"][-OVERLAP_SIZE:]
                    overlap_start = chunks[-1]["end_char"] - len(overlap_text)
                    current_chunk = overlap_text + sub_block + "\n\n"
                    chunk_start = overlap_start
                else:
                    current_chunk = sub_block + "\n\n"
                    chunk_start = sub_start

            prev_end = sub_end
            cursor = sub_end

    # last chunk
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "start_char": chunk_start,
            "end_char": prev_end
        })

    # filter
    chunks = [c for c in chunks if len(c["content"]) >= MIN_CHUNK_SIZE]

    return chunks