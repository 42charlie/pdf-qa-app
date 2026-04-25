function UserMessage({ message }) {
	return (
		<div className="self-end max-w-[85%]">
			<div className="bg-slate-800 text-sm text-white px-4 py-3 rounded-lg rounded-tr-none shadow-sm">
				{message}
			</div>
		</div>
  );
}

export default UserMessage;