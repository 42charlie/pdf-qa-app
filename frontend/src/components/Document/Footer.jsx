import { FiInfo } from "react-icons/fi";

function Footer({ chunkInfo }) {
	return (
		<div className="w-full h-8 bg-slate-50 flex px-5 py-3 justify-between border-b border-slate-200">
				{ chunkInfo ? (
					<>
					<div className="flex items-center">
						<span className="text-[10px] font-mono text-slate-400">Chunk id: {chunkInfo?.id != null ? chunkInfo.id : 'N/A'}</span>
					</div>
					<div className="flex items-center">
						<span className="text-[10px] font-mono text-slate-400">Start Char: {chunkInfo?.start != null ? chunkInfo.start : 'N/A'}</span>
					</div>
					<div className="flex items-center">
						<span className="text-[10px] font-mono text-slate-400">End Char: {chunkInfo?.end != null ? chunkInfo.end : 'N/A'}</span>
					</div>
					<div className="flex items-center">
						<span className="text-[10px] font-mono text-slate-400">Chunk Length: {chunkInfo?.length != null ? chunkInfo.length : 'N/A'}</span>
					</div>
					</>
				) : (
					<div className="flex items-center gap-2 text-slate-500 text-[10px] font-bold">
						<FiInfo className="w-3 h-3"/>
						<span className="uppercase tracking-wider">hover text to inspect chunks</span>
					</div>
				)}
			</div>
	);
}

export default Footer;