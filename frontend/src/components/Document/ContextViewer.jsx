import { useState, useEffect } from "react";
import { FiChevronLeft } from "react-icons/fi";

function ContextViewer({ shownChunk, setSubTab }) {
	const [isLoading, setIsLoading] = useState(true);
	const [chunkContext, setChunkContext] = useState({"before": "", "chunk": "", "after": ""});

	useEffect(() => {
		try {
			const timer = setTimeout(() => {
				setIsLoading(false);
				setChunkContext({
					before: "Curabitur rhoncus feugiat enim, ut porta diam pulvinar ut. Integer et ullamcorper dui, ac fermentum orci. Morbi porta ultricies lacus, vel dictum quam tempus eget. Ut vitae odio at sem posuere ullamcorper. Curabitur pharetra aliquet pellentesque. Fusce blandit scelerisque nisi quis facilisis. Integer quam massa, ultricies in mi eu, maximus scelerisque lacus. In diam neque, dignissim vitae malesuada non, egestas non nulla. Suspendisse potenti. Vestibulum non velit dolor. In aliquam tortor sapien, eu viverra ante imperdiet vitae. Ut porttitor ultricies tellus a varius. Nunc ultricies venenatis eleifend. Vestibulum feugiat a est ut efficitur. Duis eu lobortis quam. Maecenas fringilla dignissim lectus, sit amet feugiat nulla. Proin donec.",
					current: "Vestibulum et ex pellentesque, vulputate diam a, dignissim velit. Maecenas eu luctus urna. Ut vulputate vitae est at sagittis. Donec vulputate pulvinar odio, a scelerisque sem sollicitudin in. Fusce gravida felis at ex congue, in auctor neque rutrum. Duis lectus magna, lobortis vitae fringilla non, pulvinar at lectus. Nunc eu lacus finibus elit tempor tincidunt tempus suscipit est. Nullam nec est vel libero sollicitudin iaculis. Cras finibus varius sem, a interdum neque. Duis sed pharetra urna, non tincidunt nibh. Nam aliquet sem ut purus accumsan, quis molestie tellus semper. Donec elit purus, vulputate eu ipsum ac, ultrices interdum est. Aenean ullamcorper rhoncus pretium. Maecenas ut tristique nibh, a porta massa. Fusce et viverra.",
					after: "Donec eget nisl pellentesque, varius lorem sit amet, consequat nisi. Sed justo lacus, scelerisque et augue nec, feugiat varius elit. Donec tristique iaculis accumsan. Cras vestibulum arcu ac volutpat gravida. Vestibulum lobortis pellentesque cursus. Donec ac vehicula mi, vel mattis tellus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum dui nunc, laoreet sit amet suscipit at, ultrices at elit. Mauris pulvinar tortor dui, non semper lacus maximus et. Morbi convallis congue felis luctus facilisis. Integer tortor risus, tempor ut nibh sit amet, accumsan rhoncus eros. Ut accumsan, libero in convallis tempor, ante lorem tincidunt purus, ac ornare enim nulla sed sapien. Vivamus amet."
				})
			}, 1000);

			return () => clearTimeout(timer);
		} catch (error) {
			console.error("Error loading chunk content:", error);
			setIsLoading(false);
		}
	}, [shownChunk]);
	return (
		<div className="flex flex-col gap-3 h-full overflow-hidden">
			
			<span 
				onClick={() => setSubTab("list")} 
				className="self-start flex flex-row items-center hover:bg-slate-100 rounded-md gap-1 p-1 px-2 cursor-pointer text-[10px] uppercase font-sans font-bold"
			>
					<FiChevronLeft/>
					Back to chunk list
			</span>

			<div className="flex-1 overflow-y-auto min-h-0 bg-white text-sm text-slate-600 font-mono whitespace-pre-wrap pr-2">
				{ isLoading ? (
					<div className="animate-pulse space-y-3">
						<div className="h-4 bg-slate-100 rounded w-full"></div>
						<div className="h-4 bg-slate-100 rounded w-5/6"></div>
						<div className="h-4 bg-slate-100 rounded w-4/6"></div>
					</div>
				) : (
					<>
						<span className="py-0.5">{chunkContext.before}</span>
						<span className="py-0.5 bg-blue-100 text-blue-900">{chunkContext.current}</span>
						<span className="py-0.5">{chunkContext.after}</span>
					</>
				)}
			</div>
		</div>
	);
}

export default ContextViewer;