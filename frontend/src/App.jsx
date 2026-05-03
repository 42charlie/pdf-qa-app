import Banner from "./components/Banner";
import Document from "./components/Document";
import Chat from "./components/Chat";
import Upload from "./components/Upload";
import { useState } from "react";

function App() {
	const [retrievedChunks, setRetrievedChunks] = useState(null);
	const [activeTab, setActiveTab] = useState("text");
	const [page, setPage] = useState("home");
	const [metadata, setMetadata] = useState(null);

	return (
		<div className="bg-white h-screen flex overflow-hidden">
			<Banner />
			{ page === "document" ? (
				<>
				<Document retrievedChunks={retrievedChunks} setPage={setPage} setActiveTab={setActiveTab} activeTab={activeTab} metadata={metadata} />
				<Chat setRetrievedChunks={setRetrievedChunks} setActiveTab={setActiveTab}/>
				</>
			) : <Upload setPage={setPage} setMetadata={setMetadata} /> }

		</div>
	);
}

export default App;