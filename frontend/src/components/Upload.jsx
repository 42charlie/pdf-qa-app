import { FaRegFileAlt } from "react-icons/fa";
import { IoCloudUploadOutline } from "react-icons/io5";


function Upload () {
	return (
		<div className="relative flex bg-slate-50 h-screen w-screen justify-around">
			<div class="absolute top-[-5%] left-[-5%] w-[40%] h-[40%] rounded-full bg-blue-400/10 blur-[100px] pointer-events-none"></div>
        	<div class="absolute bottom-[-5%] right-[-5%] w-[40%] h-[40%] rounded-full bg-indigo-400/10 blur-[100px] pointer-events-none"></div>
			<div className="flex flex-col p-5 gap-14 justify-center items-center max-w-2xl">
				<div className="flex flex-col gap-3 w-full">
					<h1 className="text-3xl font-bold self-center text-slate-700">Document Intelligence</h1>
					<div className="self-center text-center w-full text-slate-500 text-sm px-3">Upload a document to instantly process its chunks, view contextual relationships, and generate fully grounded answers.</div>
				</div>
				<div className="flex flex-col gap-5 bg-white rounded-3xl py-10 items-center w-full border-2 border-dashed border-slate-300 hover:bg-slate-50 hover:border-blue-400 duration-300 group">
					<div className="flex h-30 w-30 items-center justify-center">
						<div className="flex items-center justify-center bg-blue-50 h-20 w-20 rounded-full text-blue-400 group-hover:h-22 group-hover:w-22 duration-300">
								<IoCloudUploadOutline className="h-8 w-8 group-hover:h-10 group-hover:w-10 duration-300"/>
						</div>
					</div>
					<div className="flex flex-col gap-1 items-center">
						<div className="font-bold text-lg text-slate-600">Click to upload document</div>
						<div className="text-sm font-medium text-slate-400">or drag and drop it here</div>
					</div>
					<div className="flex flex-row gap-2 text-[10px] font-mono text-slate-400">
						<div className="px-3 py-1 rounded-md bg-slate-100 border border-slate-200">PDF</div>
						<div className="px-3 py-1 rounded-md bg-slate-100 border border-slate-200">Max 3MB</div>
					</div>
				</div>
				<div className="space-y-3 w-full">
					<div className="font-semibold text-xs text-slate-400">RECENT DOCUMENTS</div>
					<div className="flex-col gap-1 bg-white p-4 rounded-xl border border-slate-200 hover:border-slate-300 duration-300 group">
						<div className="flex justify-between">
							<div className="flex flex-row gap-3">
								<div className="p-3 bg-red-50 rounded-lg">
									<FaRegFileAlt className="text-red-400"/>
								</div>
								<div className="flex flex-col text-sm gap-0.5">
									<span className="font-semibold text-slate-500 group-hover:text-blue-500 duration-300">financial_report_2023.pdf</span>
									<span className="text-slate-400 text-[10px] font-medium font-mono">Processed 2 hours ago • 14 Chunks</span>
								</div>
							</div>
							<div className="text-slate-400">
								<button className="py-2 px-4 text-[11px] font-semibold hover:text-slate-600 rounded-lg border border-slate-200 opacity-0 group-hover:opacity-100 hover:bg-slate-50 duration-300">Open Workspace</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Upload;