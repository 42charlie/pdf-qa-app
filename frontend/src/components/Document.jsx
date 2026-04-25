import Header from "./DocumentHeader";

function Document() {
  return (
	<div className="w-3/5 bg-white overflow-hidden overflow-y-auto flex flex-col border-r border-slate-200">
		<Header />
		
	</div>
  );
}

export default Document;