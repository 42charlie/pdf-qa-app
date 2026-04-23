import { Upload, Document, TextExtraction, Chunks, Question, Retrieval, Answer } from "./VisualVariants";

const VISUAL_COMPONENTS = {
  'upload': Upload,
  'document': Document,
  'text': TextExtraction,
  'chunks': Chunks,
  'question': Question,
  'retrieval': Retrieval,
  'answer': Answer
};

function StickyVisualizer({ activeStep }) {
  const VisualComponent = VISUAL_COMPONENTS[activeStep] || Upload; // Default visual

  return (
	<div className="sticky top-0 flex-1 h-screen px-10 py-20">
	  <h2 className="text-xl font-bold"><VisualComponent /></h2>
	</div>
  );
}

export default StickyVisualizer;