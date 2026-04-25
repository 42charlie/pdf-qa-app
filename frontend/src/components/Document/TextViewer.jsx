function TextViewer({ text, chunks }) {
	return (
		<div className="overflow-y-auto bg-white p-6 text-sm text-slate-600 font-mono whitespace-pre-wrap">
			{text}
		</div>
	)}

export default TextViewer;