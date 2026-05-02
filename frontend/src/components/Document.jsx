import Footer from "./Document/Footer";
import Header from "./Document/Header";
import TextViewer from "./Document/TextViewer";
import RetrievedChunks from "./Document/RetrievedChunks";
import { useState } from "react";

//mock data - to be replaced with actual data from backend
const text = `Donec ut rhoncus ex. Fusce ut mattis enim, pellentesque vehicula ante. Sed tincidunt at turpis vulputate finibus. Proin lobortis tincidunt maximus. Cras ac risus eu eros scelerisque placerat vitae eu ligula. Nullam feugiat finibus orci quis lacinia. Sed vehicula in tortor ac semper. Aliquam et arcu dignissim, porttitor sem et, fringilla lectus. Integer sit amet nisl massa. Maecenas rhoncus ac tortor id rhoncus. Pellentesque pellentesque risus ut efficitur convallis. Pellentesque id est finibus, feugiat sem ac, interdum risus. Fusce sapien ante, accumsan at lacus eget, condimentum laoreet mi. Suspendisse lobortis at elit non semper.

Aliquam erat volutpat. Aliquam id vehicula dui. Donec at arcu ut libero convallis faucibus. Nam sit amet lorem vehicula justo eleifend fringilla. Sed ligula diam, tempus at tortor vel, molestie faucibus lorem. Nam commodo orci vel metus fermentum mollis. Vestibulum varius nisi sit amet turpis porta, in congue purus egestas. Vivamus molestie dolor in massa aliquet auctor. Pellentesque nec sem pellentesque, auctor nisi vitae, fringilla enim. Duis ac maximus nisl. Donec leo justo, hendrerit in mollis sit amet, condimentum non velit.

Nullam id gravida mauris. Fusce luctus elementum tortor nec sagittis. Nunc fringilla posuere consequat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut tellus nibh, convallis ut augue eget, laoreet semper enim. Quisque id nunc efficitur, dapibus nulla ornare, vestibulum turpis. Curabitur aliquet orci ut ipsum iaculis, a cursus massa pulvinar. Mauris quis commodo eros. Donec sit amet scelerisque enim. Integer tortor ipsum, gravida et euismod ut, condimentum sed erat. Curabitur lacinia, dolor bibendum vestibulum ullamcorper, tellus arcu ultricies est, et aliquam orci nulla eget diam. Aenean scelerisque tincidunt tempor. Donec erat nunc, rutrum in turpis ut, hendrerit imperdiet arcu. Suspendisse sit amet tincidunt ligula.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sit amet aliquet tellus. Nam quis imperdiet velit. Nunc aliquet euismod volutpat. Proin mi turpis, tincidunt ac lacus ut, finibus rutrum purus. Aliquam nunc purus, tincidunt vel urna ut, vulputate venenatis nisi. Curabitur pellentesque ligula et consectetur laoreet. Mauris faucibus nulla est, quis dapibus enim lacinia at. Duis suscipit convallis blandit. Nam a magna augue. Curabitur vehicula facilisis lorem sit amet ornare. Maecenas vulputate lacus eget lorem convallis, at venenatis ante sagittis. Nunc tempus, mauris a pretium sodales, augue erat laoreet nibh, nec posuere tortor tortor ut neque. Sed porttitor, sapien ut laoreet congue, elit odio egestas nibh, quis tincidunt dolor lacus vel nisi.The compliance team has allocated a $2.4M budget to address these concerns by EOY. Furthermore, malicious inputs previously used to bypass the system have been identified and mitigated, ensuring the integrity of our operations moving forward.`;

const chunks = [
	{ id: 0, length: 500, start: 0, end: 500 },
	{ id: 1, length: 600, start: 500, end: 1100 },
	{ id: 2, length: 450, start: 1100, end: 1550 },
	{ id: 3, length: 700, start: 1550, end: 2250 },
	{ id: 4, length: 300, start: 2250, end: 2550 },
	{ id: 5, length: 800, start: 2550, end: 3350 },
	{ id: 6, length: 400, start: 3350, end: 3750 },
	{ id: 7, length: 550, start: 3750, end: 4300 },
	{ id: 8, length: 650, start: 4300, end: 4950 },
	{ id: 9, length: 350, start: 4950, end: 5300 },
]
//end of mock data

function Document( { retrievedChunks, setActiveTab, activeTab, metadata } ) {
	const [chunkInfo, setChunkInfo] = useState(null);

	return (
		<div className="w-3/5 bg-white overflow-hidden flex flex-col border-r border-slate-200">
			<Header setActiveTab={setActiveTab} activeTab={activeTab} metadata={metadata} />
			{ activeTab === 'text' ?
			<>
				<TextViewer activeTab={activeTab} text={text} chunks={chunks} setChunkInfo={setChunkInfo} />
				<Footer chunkInfo={chunkInfo}/>
			</> : <RetrievedChunks retrievedChunks={retrievedChunks}/> }
		</div>
	);
}

export default Document;