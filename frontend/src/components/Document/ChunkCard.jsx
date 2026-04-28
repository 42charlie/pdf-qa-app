import { useState, useRef, useEffect } from "react";
import { FiChevronRight, FiChevronDown, FiChevronUp } from "react-icons/fi";

function ChunkCard({ index, chunk, setSubTab, setShownChunk }) {
	let score = "";
	const [expanded, setExpanded] = useState(false);
	const [isTruncated, setIsTruncated] = useState(false);

	if (index === 0) score = "text-emerald-600 bg-emerald-50 border-emerald-100";
	else if (index === 1) score = "text-amber-600 bg-amber-50 border-amber-100";
	else score = "text-slate-600 bg-slate-50 border-slate-200 ";

	const textRef = useRef(null);

	useEffect(() => {
		const element = textRef.current;
		if (!element) return;

		if (element.scrollHeight > element.clientHeight) {
			setIsTruncated(true);
		}
	}, [chunk.preview]); // Re-run if the text ever changes

	function HandleShowConext() {
		setSubTab("context");
		setShownChunk(chunk);
	}

	return (
		<div
			key={index}
			className={`group flex flex-col gap-2 rounded-xl border border-slate-200 p-4 hover:shadow-sm ${isTruncated ? "pb-1" : ""}`}
		>
			<div className="flex justify-between text-sm text-black">
				<div className="flex gap-2 text-[10px]">
					<span className="rounded-md border border-slate-200 bg-slate-50 px-2 py-1.5 font-sans text-slate-600 font-extrabold">
						#{chunk.id}
					</span>
					<span className={`rounded-md border px-2 py-1.5 ${score}`}>
						Score: {chunk.dist}
					</span>
				</div>
				<button onClick={HandleShowConext} className="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-slate-50 px-2 py-1.5 font-sans text-[10px] font-bold text-slate-400 duration-300 group-hover:text-slate-600 hover:border-blue-200 hover:bg-slate-100 hover:text-blue-600">
					Show context
					<FiChevronRight />
				</button>
			</div>
			<div className="pt-2 font-mono leading-relaxed text-slate-600">
				<p className={expanded ? "" : "line-clamp-5"} ref={textRef}>
					{chunk.preview}
				</p>
				<div
					className={`mt-1 flex cursor-pointer items-center justify-center gap-1 font-sans text-[11px] text-slate-300 transition-colors duration-300 hover:text-blue-600 ${isTruncated ? "block" : "hidden"}`}
					onClick={() => setExpanded(!expanded)}
				>
					{expanded ? <FiChevronUp /> : <FiChevronDown />}
					<p>{expanded ? "less" : "more"}</p>
				</div>
			</div>
		</div>
	);
}

export default ChunkCard;
