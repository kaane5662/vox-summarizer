export default function SummarySection({Sections}){
    return(
        <div className="flex flex-col gap-4 leading-[40px]">
            {Sections?.map((section:String,index)=>{
                let content;
                if (section.startsWith('s')) {
                    // Summary content
                    content = <p key={index}><strong>Summary:</strong> {section.slice(1)}</p>;
                } else if (section.startsWith('h') && !section.startsWith('hs')) {
                    // Heading content
                    content = <h2 className="font-bold" key={index}>{section.slice(1)}</h2>;
                } else if (section.startsWith('hs')) {
                    // Header paragraph content
                    content = <p key={index}>{section.slice(2)}</p>;
                } else {
                    // Unknown type, handle accordingly
                    content = <span></span>;
                }
                return content;
            })}
            {/* <h3 className="text-3xl font-bold">Summary</h3>
            <p className="leading-10">{ArticleSummary?.summary}</p> */}
            
        </div>
    )
}