import ChunkCard from "./ChunkCard";

function ChunkList({ retrievedChunks, setShownChunk, setSubTab }) {
	return (
			<div className="space-y-5">
				{retrievedChunks.map((chunk, index) => (
					<ChunkCard key={index} index={index} chunk={chunk} setSubTab={setSubTab} setShownChunk={setShownChunk}/>
				))}
			</div>
	);
}

export default ChunkList;
