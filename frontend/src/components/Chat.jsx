import { IoSend } from "react-icons/io5";

function Header() {
  return (
	<div className="w-full h-10 bg-white px-5 py-3 border-b border-slate-200">
		<span className="flex text-xs font-semibold text-slate-800">Retrieval & Generation</span>
	</div>
  );
}

function Question() {
	return (
		<div className="w-full h-19 bg-white px-5 py-3 border-b border-slate-200">
			<form className="relative flex items-center gap-3 bg-slate-50 border border-slate-300 rounded-md px-3 py-2">
					<input type="text" name="question" placeholder="Ask a question about the document..." className="flex-1 h-8 bg-transparent text-slate-900 rounded-md p-3 pr-10 text-sm focus:outline-none"/>
					<button className="absolute right-2 p-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors" type="submit">
						<IoSend />
					</button>
			</form>
		</div>
	);
}

function Chat() {
  return (
	<div className="flex flex-col w-2/5 bg-slate-50 overflow-hidden overflow-y-auto">
		<Header />
		<div className="flex-1 w-full bg-slate-50 px-5 py-3 border-b border-slate-200">
		</div>
		<Question/>

	</div>
  );
}

export default Chat;