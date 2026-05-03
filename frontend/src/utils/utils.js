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

export function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    
    // Get the difference in seconds
    const diffInSeconds = Math.round((date - now) / 1000); 
    const absDiff = Math.abs(diffInSeconds);

    // Initialize the built-in formatter
    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

    // Figure out the right unit to use
    if (absDiff < 60) {
        return rtf.format(diffInSeconds, 'second'); // seconds ago
    } else if (absDiff < 3600) {
        return rtf.format(Math.round(diffInSeconds / 60), 'minute'); // minutes ago
    } else if (absDiff < 86400) {
        return rtf.format(Math.round(diffInSeconds / 3600), 'hour'); // hours ago
    } else if (absDiff < 2592000) {
        return rtf.format(Math.round(diffInSeconds / 86400), 'day'); // days ago
    } else if (absDiff < 31536000) {
        return rtf.format(Math.round(diffInSeconds / 2592000), 'month'); // months ago
    } else {
        return rtf.format(Math.round(diffInSeconds / 31536000), 'year'); // year ago
    }
}