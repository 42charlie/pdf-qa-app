import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

function Banner() {
  return (
	<div className="hidden md:flex w-full h-auto md:w-14 md:h-full bg-slate-50 flex-row md:flex-col py-2 md:py-4 border-b md:border-b-0 md:border-r border-slate-200 shrink-0 z-20">
		<div className="space-y-0 md:space-y-4 space-x-6 md:space-x-0 text-xl text-slate-400 flex flex-row md:flex-col items-center justify-center w-full mt-0 md:mt-4">
			<a href="https://github.com/42charlie/pdf-qa-app" target="_blank" rel="noopener noreferrer" className="p-2 hover:text-slate-900 transition hover:bg-slate-200 rounded-md">
				<FaGithub className="m-auto"/>
			</a>
			<a href="https://linkedin.com/in/42charlie" target="_blank" rel="noopener noreferrer" className="p-2 hover:text-sky-700 transition hover:bg-blue-50 rounded-md">
				<FaLinkedin className="m-auto"/>
			</a>
			<a href="mailto:breaksadik@gmail.com" target="_blank" rel="noopener noreferrer" className="p-2 hover:text-red-500 transition hover:bg-red-50 rounded-md">
				<FaEnvelope className="m-auto"/>
			</a>
		</div>
	</div>
  );
}

export default Banner;