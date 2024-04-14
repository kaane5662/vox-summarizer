"use client"
import { Summary } from "../types"
import { useRouter } from "next/navigation"
export default function SummaryHeader({summary}){
    const router = useRouter()

    return(
        <div onClick={()=>router.push(`/summary/${summary.article_id}`)} className="flex flex-col border-opacity-10 p-6 rounded-2xl hover:scale-105 hover:cursor-pointer duration-300 gap-2 w-[100%] bg-white bg-opacity-40 shadow-lg">
            <div className="flex gap-4 flex-wrap">
                {summary?.categories.map((category:String, index:Number)=>{
                    return(
                        <span className={`${index == 0 ? "bg-complementary": "bg-secondary bg-opacity-20"} px-4 rounded-xl font-bold text-sm max-h-fit `}>{category}</span>
                    )
                })}
                
            </div>
            <h1 className="text-xl font-bold">{summary.title.substring(0,40)+"..."}</h1>
            <h3 className="text-sm font-semibold text-opacity-50 text-secondary">{summary.author.substring(0,40)+""}</h3>
            {/* <h1 className="mt-8 text-md">By Kaan Eren</h1> */}
            
        </div>
    )
}