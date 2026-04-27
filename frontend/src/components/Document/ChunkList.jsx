import ChunkCard from "./ChunkCard";

function ChunkList({ retrievedChunks }) {
	return (
		<div className="flex flex-col gap-3">
			<div className="flex flex-row justify-between px-2 text-[10px]">
				<h2 className="font-bold text-slate-500 uppercase">Retrieved Chunks</h2>
				<span className="font-mono text-slate-400">
					{retrievedChunks.length} Chunks retrieved
				</span>
			</div>
			<div className="space-y-5">
				{retrievedChunks.map((chunk, index) => (
					<ChunkCard key={index} index={index} chunk={chunk} />
				))}
			</div>
		</div>
	);
}

export default ChunkList;
