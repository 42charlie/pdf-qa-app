import { FiUpload } from "react-icons/fi";

function Toggle({ setActiveTab, activeTab }) {
	const highlightedClass = "text-slate-800";
	const normalClass = "text-slate-500 hover:text-slate-700";
	return (
		<div className="inline-grid grid-cols-2 bg-slate-100 p-1 rounded-lg border border-slate-200 text-[10px] font-bold uppercase tracking-wider absolute top-3 z-10">
			<div 
				className={`absolute top-1 bottom-1 left-1 w-[calc(50%-4px)] bg-white rounded-md shadow-sm transition-transform duration-300 ease-out ${
					activeTab === "text" ? "translate-x-0" : "translate-x-full"
				}`}
			></div>
			<button className={`${activeTab === "text" ? highlightedClass : normalClass} z-10 px-4 py-1.5 rounded-md`} onClick={() => setActiveTab("text")}>
				Text preview
			</button>
			
			<button className={`${activeTab === "chunks" ? highlightedClass : normalClass} z-10 px-4 py-1.5 rounded-md`} onClick={() => setActiveTab("chunks")}>
				Retrieved Chunks
			</button>
		</div>)}

function Header( { documentinfo, setActiveTab, activeTab } ) {
  return (
	<>
	<div className="w-full h-10 bg-slate-50 flex px-5 py-3 justify-between border-b border-slate-200">
		<div className="flex items-center gap-3">
			<span className="text-xs font-semibold text-slate-800 max-w-[40ch] truncate">{documentinfo.name}</span>
			<span className="text-[10px] font-mono text-slate-500">{documentinfo.size} • {documentinfo.pages} Pages • {documentinfo.chunks} Chunks • {documentinfo.textLength} Character</span>
		</div>
		<div className="flex items-center">
			<button className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800"> <FiUpload /> Replace</button>
		</div>
	</div>
	<div className="w-full h-0 flex justify-center bg-transparent relative">
		<Toggle setActiveTab={setActiveTab} activeTab={activeTab}/>
	</div>
	</>
  );
}

export default Header;