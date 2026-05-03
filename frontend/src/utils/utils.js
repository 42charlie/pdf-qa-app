export function SegmentText(text, chunks) {
	// Find every start and end point in the document
	const breakpoints = new Set([0, text.length]);
	chunks.forEach(chunk => {
		breakpoints.add(Math.max(0, Math.min(chunk.start, text.length)));
		breakpoints.add(Math.max(0, Math.min(chunk.end, text.length)));
	});

	// Sort the breakpoints in ascending order
	const sortedBreakpoints = Array.from(breakpoints).sort((a, b) => a - b);
	const segments = [];
    
	for (let i = 0; i < sortedBreakpoints.length - 1; i++) {
		const start = sortedBreakpoints[i];
		const end = sortedBreakpoints[i + 1];
	
		const overlappingChunks = chunks.filter(chunk => start >= chunk.start && end <= chunk.end);
		
		const segmentText = text.slice(start, end);
		if (segmentText.length === 0) continue; // Skip empty segments

		segments.push({
			id: `${start}-${end}`,
			text: segmentText,
			chunks: overlappingChunks.map(chunk => chunk.index),
            chunksData: overlappingChunks
		});
	}

	return segments;
}