import { FaRegFileAlt } from "react-icons/fa";
import UploadArea from "./Upload/UploadArea";

function Upload({ setPage }) {

	return (
		<div className="relative flex bg-slate-50 h-screen w-screen justify-around">
			<div className="absolute top-[-5%] left-[-5%] w-[40%] h-[40%] rounded-full bg-blue-400/10 blur-[100px] pointer-events-none"></div>
        	<div className="absolute bottom-[-5%] right-[-5%] w-[40%] h-[40%] rounded-full bg-indigo-400/10 blur-[100px] pointer-events-none"></div>
			<div className="flex flex-col p-5 gap-14 justify-center items-center max-w-2xl">
				<div className="flex flex-col gap-3 w-full">
					<h1 className="text-3xl font-bold self-center text-slate-700">Document Intelligence</h1>
					<div className="self-center text-center w-full text-slate-500 text-sm px-3">Upload a document to instantly process its chunks, view contextual relationships, and generate fully grounded answers.</div>
				</div>
				<UploadArea setPage={setPage} />
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