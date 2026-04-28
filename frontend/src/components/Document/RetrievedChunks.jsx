import ChunkList from "./ChunkList";
import { BsChatDots, BsSearch } from "react-icons/bs";

function RetrievedChunks({ retrievedChunks }) {
	return (
		<div className="flex-1 overflow-hidden overflow-y-auto bg-white p-6 pt-16 font-mono text-sm whitespace-pre-wrap text-slate-600 flex flex-col">

			{retrievedChunks === null && (
				<div className="flex-1 flex flex-col items-center justify-center text-center px-6 pb-20 mt-10">
					<div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center mb-4 shadow-sm">
						<BsChatDots className="w-5 h-5 text-slate-400"/>
					</div>
					<h3 className="text-sm font-semibold text-slate-700 font-sans">Waiting for query...</h3>
					<p className="text-[11px] text-slate-400 mt-1.5 max-w-80 leading-relaxed font-sans">
						Ask a question in the chat panel to see the relevant document chunks appear here.
					</p>
				</div>
			)}

			{retrievedChunks !== null && retrievedChunks.length === 0 && (
				<div className="flex-1 flex flex-col items-center justify-center text-center px-6 pb-20 mt-10">
					<div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center mb-4 shadow-sm">
						<BsSearch className="w-4 h-4 text-slate-400"/>
					</div>
					<h3 className="text-sm font-semibold text-slate-700 font-sans">No relevant context found</h3>
					<p className="text-[11px] text-slate-400 mt-1.5 max-w-80 leading-relaxed font-sans">
						The document doesn't seem to contain information directly answering this query. Try rephrasing your question.
					</p>
				</div>
			)}

			{retrievedChunks !== null && retrievedChunks.length > 0 && (
				<ChunkList retrievedChunks={retrievedChunks} />
			)}
			
		</div>
	);
}

export default RetrievedChunks;