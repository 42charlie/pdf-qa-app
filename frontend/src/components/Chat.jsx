import { IoSend } from "react-icons/io5";
import { useState, useRef, useEffect } from "react";
import UserMessage from "./Chat/UserMessage";
import SystemMessage from "./Chat/SystemMessage";

function Header() {
  return (
	<div className="w-full h-10 bg-white px-5 py-3 border-b border-slate-200 ">
		<span className="flex text-xs font-semibold text-slate-800">Retrieval & Generation</span>
	</div>
  );
}

function Question( {inputValue, setInputValue, isThinking , onSubmit} ) {
	return (
		<div className="w-full h-19 bg-white px-5 py-3 border-b border-slate-200">
			<form className="relative flex items-center gap-3 bg-slate-50 border border-slate-300 rounded-md px-3 py-2 overflow-hidden" onSubmit={onSubmit}>
					<input type="text" name="question" placeholder="Ask a question about the document..." value={inputValue} onChange={(e) => setInputValue(e.target.value)} className="flex-1 h-8 bg-transparent text-slate-900 rounded-md p-3 pr-10 text-sm focus:outline-none"/>
					<button className={`absolute right-2 p-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors ${isThinking ? 'opacity-50 cursor-not-allowed' : ''}`} type="submit" disabled={isThinking}>
						<IoSend />
					</button>
			</form>
		</div>
	);
}

function Chat( { setRetrievedChunks, setActiveTab, metadata } ) {
	const [inputValue, setInputValue] = useState("");
	const [isThinking, setIsThinking] = useState(false);
	const [messages, setMessages] = useState([]);
	const messagesEndRef = useRef(null);

	const onsubmit = async (e) => {
		e.preventDefault();
		if (inputValue.trim() === "") return;
		const newUserMessage = {
			id: Date.now(),
			role: 'user',
			content: inputValue
		};
		setMessages([...messages, newUserMessage]);
		setInputValue("");
		setIsThinking(true);

		const formData = new FormData();
    	formData.append("uuid", metadata.id);
    	formData.append("question", inputValue);

		try {
			const response = await fetch(`${import.meta.env.VITE_API_URL}/chat/ask`,
			{
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error ||
					`Failed to submit question: ${response.status}. Please try again.`);
			}

			const data = await response.json();
			console.log("LLM Response:", data);
			const llmResponse = {
				id: Date.now(),
				role: 'system',
				error: false,
				content: data.data.answer,
				isgrounded: data.data.grounded,
				used_chunks: data.data.used_chunk_ids,
				citations: data.retrieved_chunks || []
			};
			console.log("citations:", llmResponse.citations);
			setRetrievedChunks(llmResponse.citations)
			setActiveTab('retrieved');
			setMessages(prevMessages => [...prevMessages, llmResponse]);
		} catch (error) {
			const llmResponse = {
				id: Date.now(),
				role: 'system',
				error: true,
				content: error.message || "An error occurred while getting the response. Please try again.",
				isgrounded: false,
				used_chunks: [],
				citations: []
			};
			setMessages(prevMessages => [...prevMessages, llmResponse]);
			setRetrievedChunks([])
			console.error("Error getting LLM response:", error);
		} finally {
			setIsThinking(false);
		}
		
	};

	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages, isThinking]);

  return (
	<div className="flex flex-col w-2/5 bg-slate-50 overflow-hidden">
		<Header />
		<div className="flex flex-col flex-1 gap-6 w-full bg-slate-50 px-5 py-3 border-b border-slate-200 overflow-y-auto">
			{messages.map((msg) => (
				msg.role === 'user' ? <UserMessage key={msg.id} message={msg.content} /> : <SystemMessage key={msg.id} msg={msg} />
			))}
			{isThinking && <SystemMessage isThinking={true} />}
		<span ref={messagesEndRef}></span>
		</div>
		<Question inputValue={inputValue} setInputValue={setInputValue} isThinking={isThinking} onSubmit={onsubmit} />

	</div>
  );
}

export default Chat;