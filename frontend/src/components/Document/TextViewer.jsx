import { useState, useMemo } from "react";
import { SegmentText } from "../../utils/utils.js";

function TextViewer({ text, chunks, setChunkInfo }) {
	const [activeChunkId, setactiveChunkId] = useState(null);
	const segments = useMemo(() => SegmentText(text, chunks), [text, chunks]);

	const handleMouseOver = (event, segment) => {
		if (segment.chunks.length == 0) return;

		const primaryChunkId = segment.chunks[0];
		const pimaryChunkData = segment.chunksData[0];
		
		setactiveChunkId(primaryChunkId);
		setChunkInfo(pimaryChunkData);
	}

	const handleMouseOut = () => {
		setactiveChunkId(null);
		setChunkInfo(null);
	}
	return (
		<div className="overflow-y-auto flex-1 overflow-hidden bg-white p-6 text-sm text-slate-600 font-mono whitespace-pre-wrap">
			{segments.map((segment) => {
			// Determine if this specific segment should be highlighted
			const isHighlighted = activeChunkId !== null && segment.chunks.includes(activeChunkId);

			let highlightClass = "";
			if (isHighlighted) {
				highlightClass = "bg-blue-100 text-blue-900 transition-colors duration-150";
			}

			return (
				<span
					key={segment.id}
					className={`py-0.75 ${highlightClass} ${segment.chunks.length > 0 ? 'cursor-pointer' : ''}`}
					onMouseEnter={(e) => handleMouseOver(e, segment)}
					onMouseLeave={handleMouseOut}
				>
					{segment.text}
				</span>
			);
			})}

		</div>
	)}

export default TextViewer;