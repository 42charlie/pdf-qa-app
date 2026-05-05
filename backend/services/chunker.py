import re
from config import CHUNK_SIZE, OVERLAP_SIZE, MIN_CHUNK_SIZE

def chunk_text(text: str):
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + CHUNK_SIZE
        
        if end >= text_length:
            cut_pos = text_length
        else:
            # Look backwards from the 'end' limit for a safe place to cut
            search_start = max(start + MIN_CHUNK_SIZE, end - 300)
            
            # try to cut cleanly at a paragraph break
            cut_pos = text.rfind("\n\n", search_start, end)
            
            # try to cut at a sentence boundary
            if cut_pos == -1:
                cut_pos = text.rfind(". ", search_start, end)
                if cut_pos == -1:
                    cut_pos = text.rfind(".\n", search_start, end)
                if cut_pos != -1:
                    cut_pos += 1  # Include the period in the chunk!
                    
            # try to cut at a word boundary 
            if cut_pos == -1:
                # we must check for \n, not just spaces!
                space_pos = text.rfind(" ", search_start, end)
                newline_pos = text.rfind("\n", search_start, end)
                cut_pos = max(space_pos, newline_pos)
                
            # Hard cut fallback (Extremely rare)
            if cut_pos == -1:
                cut_pos = end

        # Extract the raw chunk
        chunk_str = text[start:cut_pos]
        
        # Save it if it meets the minimum size requirements
        if len(chunk_str.strip()) >= MIN_CHUNK_SIZE:
            
            #calculate EXACT start/end characters for perfect UI highlighting
            actual_start = start + (len(chunk_str) - len(chunk_str.lstrip()))
            actual_end = cut_pos - (len(chunk_str) - len(chunk_str.rstrip()))
            
            chunks.append({
                "content": text[actual_start:actual_end],
                "start_char": actual_start,
                "end_char": actual_end
            })

        if end >= text_length:
            break
            
        # Move backwards by OVERLAP_SIZE, but ensure we keep moving forward
        next_start = max(start + 1, cut_pos - OVERLAP_SIZE)
        
        # snap forward to the next whitespace to guarantee we never start mid-word
        match = re.search(r'\s', text[next_start:cut_pos])
        if match:
            start = next_start + match.end()
        else:
            start = next_start
            
    return chunks