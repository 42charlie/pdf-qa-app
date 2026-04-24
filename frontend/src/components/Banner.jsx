import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

function Banner() {
  return (
	<div className="w-14 bg-slate-50 flex-col py-4 border-r border-slate-200">
		<div className="space-y-4 text-xl text-slate-400 flex flex-col items-center mt-4">
			<a href="https://github.com/42charlie/pdf-qa-app" target="_blank" rel="noopener noreferrer" className="p-2 hover:text-slate-900 transition hover:bg-slate-200 rounded-md">
				<FaGithub className="m-auto"/>
			</a>
			<a href="https://linkedin.com/42charlie" target="_blank" rel="noopener noreferrer" className="p-2 hover:text-sky-700 transition hover:bg-blue-50 rounded-md">
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