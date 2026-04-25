import { useState } from 'react'
import CitationCard from "./CitationCard";

function CitationPanel({ isgrounded, citations }) {
	const [showCitations, setShowCitations] = useState(true);
	return (
		<div className="bg-slate-100 rounded-lg flex-col border border-slate-200 overflow-hidden">
			<div className="flex bg-slate-50 justify-between p-3 cursor-pointer" title="hide citations" onClick={() => setShowCitations(!showCitations)}>
				<div className="flex gap-2 items-center">
					<div className={`rounded-full w-2 h-2 ${isgrounded ? 'bg-green-600' : 'bg-red-600'}`}></div>
					<span className="text-[10px] text-slate-500 uppercase font-bold">{isgrounded ? 'Grounded Response' : 'Not Grounded Response'}</span>
				</div>
				<span className="text-[10px] text-slate-400 font-mono"> {citations.length} chunks retrieved</span>
			</div>
			{isgrounded && showCitations && (
				<div className="bg-white flex-1 flex-row space-y-3 p-4  border-t border-slate-200">
						{citations.map((citation) => (
							<CitationCard key={citation.id} chunkId={citation.id} distance={citation.dist} text={citation.preview} />
						))}
				</div>
				)}
		</div>
	);
}

export default CitationPanel;