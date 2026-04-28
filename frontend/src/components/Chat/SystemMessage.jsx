import SystemMessageFooter from "./SystemMessageFooter";

function ThinkingIndicator() {
  return (
      <div className="flex gap-0.5">
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]" />
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]" />
        <div className="w-1 h-1 bg-blue-600 rounded-full animate-bounce" />
      </div>
  );
}

function SystemMessage({ message, isgrounded, citations, isThinking=false}) {
	return (
		<div className="self-start max-w-[90%]">
			<div className="bg-white text-sm leading-relaxed text-slate-800 px-4 py-3 rounded-lg rounded-tl-none shadow-sm space-y-3">
				<div>
          { isThinking ? <ThinkingIndicator /> : message}
        </div>
          { isThinking ? "" : <SystemMessageFooter isgrounded={isgrounded} citations={citations} /> }
      </div>
		</div>
  );
}

export default SystemMessage;