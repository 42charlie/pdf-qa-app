import { useState, useEffect } from "react";
import { FiChevronLeft } from "react-icons/fi";

function ContextViewer({ shownChunk, setSubTab, metadata }) {
	const [error, setError] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [chunkContext, setChunkContext] = useState({"context": "", "start_char": 0, "end_char": 0});

	useEffect(() => {
		const fetchContext = async () => {
			setIsLoading(true);
			try {
				const response = await fetch(
					`${import.meta.env.VITE_API_URL}/documents/${metadata.id}/${shownChunk.index}/context`,
					{
						method: "GET",
					}
				);

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error || `Failed to get chunk context: ${response.status}. Please try again.`);
				}

				const data = await response.json();
				console.log("Fetched chunk context:", data);
				setChunkContext(data.context);
			} catch (error) {
				setError(error);
				console.error("Error getting chunk context:", error);
			} finally {
				setIsLoading(false);
			}
		};

		fetchContext();
	}, [shownChunk]);
	return (
		<div className="flex flex-col gap-3 h-full overflow-hidden">
			
			<span 
				onClick={() => setSubTab("list")} 
				className="self-start flex flex-row items-center hover:bg-slate-100 rounded-md gap-1 p-1 px-2 cursor-pointer text-[10px] uppercase font-sans font-bold"
			>
					<FiChevronLeft/>
					Back to chunk list
			</span>

			<div className="flex-1 overflow-y-auto min-h-0 bg-white text-sm text-slate-600 font-mono whitespace-pre-wrap pr-2">
				{ isLoading || error ? (error ? (
					<div className="text-red-500 mt-4 bg-red-100 p-3 rounded">
						{error.message}
					</div>
				) : (
					<div className="animate-pulse space-y-3">
						<div className="h-4 bg-slate-100 rounded w-full"></div>
						<div className="h-4 bg-slate-100 rounded w-5/6"></div>
						<div className="h-4 bg-slate-100 rounded w-4/6"></div>
					</div>
				)) : (
					<>
						<span className="py-0.5">{chunkContext?.text?.slice(0, shownChunk.start_char - chunkContext.start_char)}</span>
						<span className="py-0.5 bg-blue-100 text-blue-900">{chunkContext?.text?.slice(shownChunk.start_char - chunkContext.start_char, shownChunk.end_char - chunkContext.start_char)}</span>
						<span className="py-0.5">{chunkContext?.text?.slice(shownChunk.end_char - chunkContext.start_char)}</span>
					</>
				)}
			</div>
		</div>
	);
}

export default ContextViewer;