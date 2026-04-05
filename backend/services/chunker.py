
CHUNK_SIZE = 800
OVERLAP_SIZE = 120
MIN_CHUNK_SIZE = 100

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
    # Step 1: split into paragraph-like blocks
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]

    chunks = []
    current_chunk = ""

    for block in blocks:
        # Step 2: handle very large blocks
        if len(block) > CHUNK_SIZE:
            sub_blocks = split_large_block(block, CHUNK_SIZE)
        else:
            sub_blocks = [block]

        for sub_block in sub_blocks:
            # Try to add to current chunk
            if len(current_chunk) + len(sub_block) + 2 <= CHUNK_SIZE:
                current_chunk += sub_block + "\n\n"
            else:
                # Save current chunk if valid
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Start new chunk WITH overlap
                if chunks:
                    overlap = chunks[-1][-OVERLAP_SIZE:]
                    current_chunk = overlap + sub_block + "\n\n"
                else:
                    current_chunk = sub_block + "\n\n"

    # Add last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Step 3: filter tiny chunks
    chunks = [c for c in chunks if len(c) >= MIN_CHUNK_SIZE]

    return chunks