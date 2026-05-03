import Footer from "./Document/Footer";
import Header from "./Document/Header";
import TextViewer from "./Document/TextViewer";
import RetrievedChunks from "./Document/RetrievedChunks";
import { useState } from "react";

function Document( { retrievedChunks, setActiveTab, activeTab, metadata, setPage } ) {
	const [chunkInfo, setChunkInfo] = useState(null);

	return (
		<div className="w-3/5 bg-white overflow-hidden flex flex-col border-r border-slate-200">
			<Header setActiveTab={setActiveTab} activeTab={activeTab} setPage={setPage} metadata={metadata} />
			{ activeTab === 'text' ?
			<>
				<TextViewer activeTab={activeTab} metadata={metadata} setChunkInfo={setChunkInfo} />
				<Footer chunkInfo={chunkInfo}/>
			</> : <RetrievedChunks retrievedChunks={retrievedChunks}/> }
		</div>
	);
}

export default Document;