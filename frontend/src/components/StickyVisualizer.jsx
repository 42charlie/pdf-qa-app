
function StickyVisualizer({ step = 0 }) {
  return (
	<div className="sticky top-0 bg-gray-300 flex-1 h-screen">
	  <h2 className="text-xl font-bold">{step}</h2>
	</div>
  );
}

export default StickyVisualizer;