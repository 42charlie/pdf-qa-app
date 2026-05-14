import { FaRegFileAlt } from "react-icons/fa";
import UploadArea from "./Upload/UploadArea";
import { timeAgo } from "../utils/utils.js";
import { useEffect, useState } from "react";

function Upload({ setPage, setMetadata, setRetrievedChunks }) {
	const [docInfo, setDocInfo] = useState(null);
	const [lastDocumentId, setLastDocumentId] = useState(localStorage.getItem('last_document'));

	setRetrievedChunks(null); //clear retrieved chunks when on upload page
	useEffect(() => {
		const fetchRecentDocument = async () => {
			try {
				const response = await fetch(
					`${import.meta.env.VITE_API_URL}/documents/${lastDocumentId}/info`,
					{
						method: "GET",
					}
				);

				if (!response.ok) {
					throw new Error(`Failed to get preview: ${response.status}.`);
				}

				const data = await response.json();
				setDocInfo(data.metadata);
			} catch (error) {
				console.error(error);
			}
		};

		if (lastDocumentId) {
			fetchRecentDocument();
		}
	}, [lastDocumentId]);

	function handleOpenWorkspace() {
		if (docInfo?.id) {
			setPage("document");
			setMetadata(docInfo);
		}
	}

	return (
		// FIX 1: Changed w-screen to w-full and added overflow-hidden to prevent horizontal scrolling
		<div className="relative flex bg-slate-50 h-screen w-full justify-center overflow-hidden">
			<div className="absolute top-[-5%] left-[-5%] w-[40%] h-[40%] rounded-full bg-blue-400/10 blur-[100px] pointer-events-none"></div>
        	<div className="absolute bottom-[-5%] right-[-5%] w-[40%] h-[40%] rounded-full bg-indigo-400/10 blur-[100px] pointer-events-none"></div>
			
			<div className="flex flex-col p-5 gap-8 justify-center items-center max-w-2xl w-full">
				<div className="flex flex-col gap-3 w-full">
					<h1 className="text-3xl font-bold self-center text-slate-700 text-center">Document Intelligence</h1>
					<div className="self-center text-center w-full text-slate-500 text-sm px-3">Upload a document to instantly process its chunks, view contextual relationships, and generate fully grounded answers.</div>
				</div>
				<UploadArea setPage={setPage} setMetadata={setMetadata} />
				
				<div className="space-y-3 w-full min-w-0">
					{docInfo && (
					<>
					<div className="font-semibold text-xs text-slate-400">RECENT DOCUMENTS</div>
						<div className="flex flex-col gap-1 bg-white p-4 rounded-xl border border-slate-200 hover:border-slate-300 duration-300 group w-full overflow-hidden">
							
							<div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-4 w-full">
								
								<div className="flex flex-row gap-3 flex-1 min-w-0 items-center w-full">
									<div className="p-3 bg-red-50 rounded-lg shrink-0">
										<FaRegFileAlt className="text-red-400"/>
									</div>
									
									<div className="flex flex-col text-sm gap-0.5 flex-1 min-w-0">
										<span className="font-semibold text-slate-500 group-hover:text-blue-500 duration-300 truncate block">
											{docInfo?.filename || "Unnamed Document"}
										</span>
										<span className="text-slate-400 text-[10px] font-medium font-mono truncate block">
											Processed {timeAgo(docInfo?.created_at)} • {docInfo?.chunk_count || 0} Chunks
										</span>
									</div>
								</div>

								<div className="text-slate-400 w-full sm:w-auto shrink-0">
									<button 
										className="w-full sm:w-auto py-2 px-4 text-[11px] font-semibold hover:text-slate-600 rounded-lg border border-slate-200 opacity-100 sm:opacity-0 group-hover:opacity-100 hover:bg-slate-50 duration-300 transition-all" 
										onClick={handleOpenWorkspace}
									>
										Open Workspace
									</button>
								</div>
								
							</div>
						</div>
					</>
					)}
				</div>
			</div>
		</div>
	);
}

export default Upload;