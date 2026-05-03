import { useState, useMemo, useEffect } from "react";
import { SegmentText } from "../../utils/utils.js";

function TextViewer({ metadata, setChunkInfo }) {
	const [activeChunkId, setActiveChunkId] = useState(null);

	const [text, setText] = useState("");
	const [chunks, setChunks] = useState([]);
	const [error, setError] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	
	useEffect(() => {
		const fetchPreview = async () => {
			setIsLoading(true);
			try {
				const response = await fetch(
					`${import.meta.env.VITE_API_URL}/documents/${metadata.id}/preview`,
					{
						method: "GET",
					}
				);

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error || `Failed to get preview: ${response.status}. Please try again.`);
				}

				const data = await response.json();
				setText(data.text);
				setChunks(data.chunks);
			} catch (error) {
				setError(error);
				console.error("Error getting preview:", error);
			} finally {
				setIsLoading(false);
			}
		};

		if (metadata?.id) {
			fetchPreview();
		}
	}, [metadata.id]);

	const segments = useMemo(() => SegmentText(text, chunks), [text, chunks]);

	const handleMouseOver = (event, segment) => {
		if (segment.chunks.length === 0) return;

		const primaryChunkId = segment.chunks[0];
		const primaryChunkData = segment.chunksData[0];
		
		setActiveChunkId(primaryChunkId);
		setChunkInfo(primaryChunkData);
	};

	const handleMouseOut = () => {
		setActiveChunkId(null);
		setChunkInfo(null);
	};

	if (isLoading || error) {
		return (
			<div className="overflow-y-auto flex-1 overflow-hidden bg-white p-6 pt-16 text-sm text-slate-600 font-mono whitespace-pre-wrap">
				{error ? (
					<div className="text-red-500 mt-4 bg-red-100 p-3 rounded">
						{error.message}
					</div>
				) : (
					<div className="animate-pulse space-y-3">
						<div className="h-4 bg-slate-100 rounded w-full"></div>
						<div className="h-4 bg-slate-100 rounded w-5/6"></div>
						<div className="h-4 bg-slate-100 rounded w-4/6"></div>
					</div>
				)}
			</div>
		);
	}

	return (
		<div className="overflow-y-auto flex-1 overflow-hidden bg-white p-6 pt-16 text-sm text-slate-600 font-mono whitespace-pre-wrap">
			{segments.map((segment) => {
				const isHighlighted = activeChunkId !== null && segment.chunks.includes(activeChunkId);

				let highlightClass = "";
				if (isHighlighted) {
					highlightClass = "bg-blue-100 text-blue-900 transition-colors duration-150";
				}

				return (
					<span
						key={segment.id}
						// Changed py-0.75 to py-0.5 (standard Tailwind)
						className={`py-0.5 ${highlightClass} ${segment.chunks.length > 0 ? 'cursor-pointer' : ''}`}
						onMouseEnter={(e) => handleMouseOver(e, segment)}
						onMouseLeave={handleMouseOut}
					>
						{segment.text}
					</span>
				);
			})}
		</div>
	);
}

export default TextViewer;