import Footer from "./Document/Footer";
import Header from "./Document/Header";
import TextViewer from "./Document/TextViewer";
import RetrievedChunks from "./Document/RetrievedChunks";
import { useState } from "react";

function Document( { retrievedChunks, setActiveTab, activeTab, subTab, setSubTab, metadata, setPage } ) {
	const [chunkInfo, setChunkInfo] = useState(null);

	return (
		<div className="w-full md:w-3/5 h-[40%] md:h-full bg-white overflow-hidden flex flex-col border-b md:border-b-0 md:border-r border-slate-200 shrink-0">
			<Header setActiveTab={setActiveTab} activeTab={activeTab} setPage={setPage} metadata={metadata} />

			<div className={`flex flex-col flex-1 overflow-hidden ${activeTab === 'text' ? 'flex' : 'hidden'}`}>
				<TextViewer metadata={metadata} setChunkInfo={setChunkInfo} />
				<Footer chunkInfo={chunkInfo}/>
			</div>

			<div className={`flex flex-col flex-1 overflow-hidden ${activeTab !== 'text' ? 'flex' : 'hidden'}`}>
				<RetrievedChunks retrievedChunks={retrievedChunks} metadata={metadata} subTab={subTab} setSubTab={setSubTab} />
			</div>
		</div>
	);
}

export default Document;