import Banner from "./components/Banner";
import Document from "./components/Document";
import Chat from "./components/Chat";
import { useState } from "react";

function App() {
  const [retrievedChunks, setRetrievedChunks] = useState(null);
	const [activeTab, setActiveTab] = useState("text");

  return (
    <div className="bg-white h-screen flex">
      <Banner />
      <Document retrievedChunks={retrievedChunks} setActiveTab={setActiveTab} activeTab={activeTab}/>
      <Chat setRetrievedChunks={setRetrievedChunks} setActiveTab={setActiveTab}/>
    </div>
  );
}

export default App;