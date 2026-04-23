
function Section({ title, description }) {
  return (
	<div className="px-10 py-20 space-y-6 min-h-screen">
	  <h2 className="text-4xl font-bold mb-4">{title}</h2>
	  <div className="text-lg max-w-xl leading-8">{description}</div>
	</div>
  );
}

export default Section;
