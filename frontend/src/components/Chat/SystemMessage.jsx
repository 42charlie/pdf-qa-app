import CitationPanel from "./CitationPanel";

function ThinkingIndicator() {
  return (
    <div className="flex items-center gap-2 text-sm text-gray-300">
      <div className="flex gap-0.5">
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]" />
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]" />
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce" />
      </div>
    </div>
  );
}

function SystemMessage({ message, isgrounded, citations, isThinking=false}) {
	return (
		<div className="self-start max-w-[90%] space-y-3">
			<div className="bg-white text-sm leading-relaxed text-slate-800 px-4 py-3 rounded-lg rounded-tl-none shadow-sm">
				{ isThinking ? <ThinkingIndicator /> : message}
			</div>
			{ isThinking ? "" : <CitationPanel isgrounded={isgrounded} citations={citations} /> }
		</div>
  );
}

export default SystemMessage;