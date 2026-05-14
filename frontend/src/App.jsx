import Banner from "./components/Banner";
import Document from "./components/Document";
import Chat from "./components/Chat";
import Upload from "./components/Upload";
import { useState } from "react";

function App() {
	const [retrievedChunks, setRetrievedChunks] = useState(null);
	const [page, setPage] = useState("home");
	const [activeTab, setActiveTab] = useState("text");
	const [subTab, setSubTab] = useState("list");
	const [metadata, setMetadata] = useState(null);

	return (
		<div className="bg-white h-[100dvh] flex flex-col md:flex-row overflow-hidden">
			<Banner />
			{ page === "document" ? (
				<>
				<Document retrievedChunks={retrievedChunks} setPage={setPage} setActiveTab={setActiveTab} subTab={subTab} setSubTab={setSubTab} activeTab={activeTab} metadata={metadata} />
				<Chat setRetrievedChunks={setRetrievedChunks} setActiveTab={setActiveTab} setSubTab={setSubTab} metadata={metadata}/>
				</>
			) : <Upload setPage={setPage} setMetadata={setMetadata} setRetrievedChunks={setRetrievedChunks}/> }
		</div>
	);
}

export default App;