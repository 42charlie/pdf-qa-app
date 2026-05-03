import {
	IoCloudUploadOutline,
	IoAlertCircleOutline,
	IoSyncOutline,
} from "react-icons/io5";
import { useRef, useState } from "react";

function UploadArea({ setPage, setMetadata }) {
	const [isDragging, setIsDragging] = useState(false);
	const [uploadedFile, setUploadedFile] = useState(null);
	const [isUploading, setIsUploading] = useState(false);
	const [error, setError] = useState(null);
	const fileInputRef = useRef(null);

	let icon = (
		<IoCloudUploadOutline className="h-8 w-8 group-hover:h-10 group-hover:w-10 duration-300" />
	);
	let iconColors = "bg-blue-50 text-blue-400";
	let boxStyles = "border-slate-300 hover:bg-slate-50 hover:border-blue-400";
	let message = "Click to upload document";
	let subMessage = "or drag and drop it here";

	if (error) {
		icon = <IoAlertCircleOutline className="h-8 w-8" />;
		iconColors = "bg-red-50 text-red-500";
		boxStyles = "border-red-300 bg-red-50/30 hover:border-red-400";
		message = error;
		subMessage = "Click or drag to try again";
	} else if (isUploading) {
		icon = <IoSyncOutline className="h-8 w-8 animate-spin" />;
		iconColors = "bg-blue-50 text-blue-500";
		boxStyles = "border-blue-300 bg-blue-50/30 pointer-events-none";
		message = "Uploading & Processing...";
		subMessage = "Please wait";
	} else if (isDragging) {
		icon = <IoCloudUploadOutline className="h-10 w-10" />;
		iconColors = "bg-blue-100 text-blue-600";
		boxStyles = "border-blue-500 bg-blue-50/50 scale-[1.02]";
		message = "Drop document here";
		subMessage = "Release to upload";
	}

	const handleDragOver = (e) => {
		e.preventDefault();
		setError(null);
		if (!isUploading) setIsDragging(true);
	};

	const handleDragLeave = (e) => {
		e.preventDefault();
		setIsDragging(false);
	};

	const handleDrop = (e) => {
		e.preventDefault();
		setIsDragging(false);

		if (
			!isUploading &&
			e.dataTransfer.files &&
			e.dataTransfer.files.length > 0
		) {
			handleFile(e.dataTransfer.files[0]);
		}
	};

	const handleClick = () => {
		if (!isUploading) fileInputRef.current.click();
	};

	const handleFileChange = (e) => {
		if (e.target.files && e.target.files.length > 0) {
			handleFile(e.target.files[0]);
		}
	};

	const handleFile = async (file) => {
		setError(null);

		if (file.type !== "application/pdf" || file.size > 1024 * 1024 * 10) {
			setError("Please upload a PDF file under 10MB.");
			return;
		}

		setUploadedFile(file);
		setIsUploading(true);

		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch(
				`${import.meta.env.VITE_API_URL}/documents/upload`,
				{
					method: "POST",
					body: formData,
				},
			);

			if (!response.ok) {
			// Try to extract error message from response, fallback to generic message
			const errorData = await response.json();
				throw new Error(errorData.error || `Failed to upload file: ${response.status}. Please try again.`,);
			}

			const data = await response.json();

			setPage("document");
			setMetadata(data.metadata);
		} catch (error) {
			setError(error);
			console.error("Error uploading file:", error);
		} finally {
			setIsUploading(false);
		}
	};

	return (
		<div
			onDragOver={handleDragOver}
			onDragLeave={handleDragLeave}
			onDrop={handleDrop}
			onClick={handleClick}
			className={`flex flex-col gap-5 rounded-3xl py-10 items-center w-full border-2 border-dashed duration-300 cursor-pointer group ${boxStyles}`}
		>
			<div className="flex h-30 w-30 items-center justify-center pointer-events-none">
				<input
					type="file"
					accept=".pdf"
					className="hidden"
					ref={fileInputRef}
					onChange={handleFileChange}
				/>
				<div
					className={`flex items-center justify-center h-20 w-20 rounded-full group-hover:scale-110 transition-transform duration-300 ${iconColors}`}
				>
					{icon}
				</div>
			</div>

			<div className="flex flex-col gap-1 items-center pointer-events-none">
				<div
					className={`font-bold text-lg ${error ? "text-red-600" : "text-slate-600"}`}
				>
					{message}
				</div>
				<div
					className={`text-sm font-medium ${error ? "text-red-400" : "text-slate-400"}`}
				>
					{subMessage}
				</div>
			</div>

			<div className="flex flex-row gap-2 text-[10px] font-mono text-slate-400 pointer-events-none mt-2">
				<div className="px-3 py-1 rounded-md bg-slate-100 border border-slate-200">
					PDF
				</div>
				<div className="px-3 py-1 rounded-md bg-slate-100 border border-slate-200">
					Max 10MB
				</div>
			</div>
		</div>
	);
}

export default UploadArea;
