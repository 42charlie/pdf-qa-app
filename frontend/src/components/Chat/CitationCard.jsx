function CitationCard({ chunkId, distance, text }) {
	return (
		<div className="flex flex-col gap-2 bg-slate-50 p-3 rounded-md">
			<div className="flex flex-row text-center justify-between">
				<span className="text-[10px] uppercase font-mono">chunk id : {chunkId}</span>
				<span className="text-[10px] uppercase text-green-500 bg-green-100 rounded-md px-2">distance : {distance}</span>
			</div>
			<span className="text-[10px] font-mono text-slate-400">{text}</span>
		</div>
	)
}

export default CitationCard;