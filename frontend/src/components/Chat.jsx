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

function Chat( { setRetrievedChunks, setActiveTab } ) {
	const [inputValue, setInputValue] = useState("");
	const [isThinking, setIsThinking] = useState(false);
	const [messages, setMessages] = useState([]);
	const messagesEndRef = useRef(null);

	const onsubmit = (e) => {
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
		
		// Simulate response from backend
		setTimeout(() => {
			const mockLlmResponse = {
				id: 2,
				role: 'system',
				content: 'According to the document, the compliance team has allocated a $2.4M budget to address ongoing regulatory scrutiny...',
				isgrounded: true,
				citations: [{ id: 0, preview: "Donec ut rhoncus ex. Fusce ut mattis enim, pellentesque vehicula ante. Sed tincidunt at turpis vulputate finibus. Proin lobortis tincidunt maximus. Cras ac risus eu eros scelerisque placerat vitae eu ligula. Nullam feugiat finibus orci quis lacinia. Sed vehicula in tortor ac semper. Aliquam et arcu dignissim, porttitor sem et, fringilla lectus. Integer sit amet nisl massa. Maecenas rhoncus ac tortor id rhoncus. Pellentesque pellentesque risus ut efficitur convallis. Pellentesque id est finibus maximus. Cras ac risus eu eros scelerisque placerat vitae eu ligula ut rhoncus ex. Fusce ut mattis enim, pellentesque vehicula ante. Sed tincidunt at turpis vulputate finibus. Proin lobortis tincidunt maximus. tortor ac semper. Aliquam et arcu tortor ac semper et arcu pellen tesque vehicula finibus .", dist: 1.150 },
							{ id: 1, preview: "feugiat sem ac, interdum risus. Fusce sapien ante, accumsan at lacus eget, condimentum laoreet mi. Suspendisse lobortis at elit non semper. Aliquam erat volutpat. Aliquam id vehicula dui. Donec at arcu ut libero convallis faucibus. Nam sit amet lorem vehicula justo eleifend fringilla. Sed ligula diam, tempus at tortor vel, molestie faucibus lorem. Nam commodo orci vel metus fermentum mollis. Vestibulum varius nisi sit amet turpis porta, in congue purus egestas.", dist: 0.750 },
							{ id: 2, preview: "Nullam id gravida mauris. Fusce luctus elementum tortor nec sagittis. Nunc fringilla posuere consequat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut tellus nibh, convallis ut augue eget, laoreet semper enim. Quisque id nunc efficitur, dapibus nulla ornare, vestibulum turpis. Curabitur aliquet orci ut ipsum iaculis, a cursus massa pulvinar.", dist: 0.550 },
			]};
			setRetrievedChunks(mockLlmResponse.citations)
			setActiveTab('retrieved');
			setMessages(prevMessages => [...prevMessages, mockLlmResponse]);
			setIsThinking(false);
		}, 2000); // Simulate a 2-second response time
	};

	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages, isThinking]);

  return (
	<div className="flex flex-col w-2/5 bg-slate-50 overflow-hidden">
		<Header />
		<div className="flex flex-col flex-1 gap-6 w-full bg-slate-50 px-5 py-3 border-b border-slate-200 overflow-y-auto">
			{messages.map((msg) => (
				msg.role === 'user' ? <UserMessage key={msg.id} message={msg.content} /> : <SystemMessage key={msg.id} isgrounded={msg.isgrounded} message={msg.content} citations={msg.citations} />
			))}
			{isThinking && <SystemMessage isThinking={true} />}
		<span ref={messagesEndRef}></span>
		</div>
		<Question inputValue={inputValue} setInputValue={setInputValue} isThinking={isThinking} onSubmit={onsubmit} />

	</div>
  );
}

export default Chat;