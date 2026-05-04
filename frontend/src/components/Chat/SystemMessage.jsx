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

function SystemMessage({ msg, isThinking=false}) {
	return (
		<div className="self-start max-w-[90%]">
			<div className={`${!isThinking && msg.error ? 'bg-red-100 text-red-500' : 'bg-white text-slate-800'} text-sm leading-relaxed px-4 py-3 rounded-lg rounded-tl-none shadow-sm space-y-3`}>
				<div>
          { isThinking ? <ThinkingIndicator /> : msg.content}
        </div>
          { isThinking ? "" : <SystemMessageFooter error={msg.error} isgrounded={msg.isgrounded} used_chunks={msg.used_chunks} /> }
      </div>
		</div>
  );
}

export default SystemMessage;