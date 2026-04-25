import { FiUpload, FiEye } from "react-icons/fi";

function Header( { documentinfo } ) {
  return (
	<>
	<div className="w-full h-10 bg-slate-50 flex px-5 py-3 justify-between border-b border-slate-200">
		<div className="flex items-center gap-3">
			<span className="text-xs font-semibold text-slate-800">{documentinfo.name}</span>
			<span className="text-[10px] font-mono text-slate-500">{documentinfo.size} • {documentinfo.pages} Pages</span>
		</div>
		<div className="flex items-center gap-2">
			<button className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800"> <FiUpload /> Replace</button>
		</div>
	</div>
	<div className="w-full h-8 bg-slate-50 flex px-5 py-3 justify-between border-b border-slate-200">
		<div className="flex items-center gap-2 text-slate-500 text-[10px] font-bold">
			<FiEye className="w-3 h-3"/>
			<span className="uppercase tracking-wider">Text chunks preview - hover to inspect</span>
		</div>
		<div className="flex items-center gap-2">
			<span className="text-[10px] font-mono text-slate-400">TEXT LENGTH: {documentinfo.textLength} / CHUNKS: {documentinfo.chunks}</span>
		</div>
	</div>
	</>
  );
}

export default Header;