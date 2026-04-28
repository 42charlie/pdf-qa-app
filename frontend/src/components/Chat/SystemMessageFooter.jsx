function SystemMessageFooter({ isgrounded, citations }) {
  return (
    <div className="flex-col overflow-hidden border-t border-slate-100">
      <div className="flex justify-between pt-2">
        <div className="flex items-center gap-2">
          <div
            className={`h-2 w-2 rounded-full ${isgrounded ? "bg-green-600" : "bg-red-600"}`}
          ></div>
          <span className="text-[10px] font-semibold text-slate-500 uppercase">
            {isgrounded ? "Grounded" : "ungrounded"} Response
          </span>
        </div>
        {isgrounded && citations.length > 0 && (
          <span className="inline-flex items-center font-mono text-[10px] text-slate-400">
            Sources:
            <div className="ml-2 flex space-x-2 font-semibold">
              {citations.map((citation) => (
                <div className="rounded-md border border-slate-200 bg-blue-50 px-1.5 py-0.5 font-semibold">
                  {" "}
                  #{citation.id}{" "}
                </div>
              ))}
            </div>
          </span>
        )}
      </div>
    </div>
  );
}

export default SystemMessageFooter;
