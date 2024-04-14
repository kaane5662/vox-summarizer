"use client"
import { useEffect, useState } from "react"
import { useRouter } from 'next/navigation';
import { Summary } from "@/app/types"
import axios from "axios";
import SummarySection from "@/app/components/SummarySection";
import VoxGPTSection from "@/app/components/VoxGPTSection";

export default function SummaryPage({params}){
    const router = useRouter();
    const {id} = params
    const [ArticleSummary, setSummary] = useState<Summary>()
    const [Sections, setSections] = useState<[]>()
    const [section, setSection] = useState(0)

    const fetchSummary = ()=>{
        console.log(process.env.SERVER_DOMAIN)
        axios.get(`http://localhost:5000/summary/${id}`).then((response)=>{
            setSummary(response.data)
            setSections(response.data.summary.split("/"))
        }).catch((error)=>{
            console.log(error.message)
        })
    }

    useEffect(()=>{
        fetchSummary()
    },[])


    return(
        <main className="min-h-screen bg-primary text-secondary flex justify-center font-cabin  ">
            <div className="flex pt-24 pb-8 flex-col gap-8 w-[60%] ">
                {/* article header */}
                <div className="flex flex-col gap-4 w-[100%] border-y-2 min-h-fit border-secondary border-opacity-20 py-4    ">
                    {/* <p>{ArticleSummary?.article_id}</p> */}
                    <div className="flex gap-8">
                        {ArticleSummary?.categories?.map((category:String, index)=>{
                            return(
                                <span className={`${index == 0 ? "bg-complementary": "bg-secondary bg-opacity-20"} py-2 px-4 rounded-xl font-bold text-sm max-h-fit `}>{category}</span>
                            )
                        })}
                        
                    </div>
                    <h1 className="text-5xl font-bold">{ArticleSummary?.title}</h1>
                    <h1 className="text-lg font-semibold text-opacity-50 text-secondary">By {ArticleSummary?.author}</h1>
                    
                    
                </div>
                <div className="flex justify-center gap-8">
                        <button onClick={()=>setSection(0)} className={`p-2 px-20 text-md border-b-[3px] ${section == 0 ? "border-complementary font-semibold": "border-opacity-10 border-secondary"}  rounded-md`}>Summary</button>
                        <button onClick={()=>{setSection(1);}} className={`p-2 px-20 text-md border-b-[3px] ${section == 1 ? "border-complementary font-semibold": "border-opacity-10 border-secondary"}  rounded-md`}>VoxGPT</button>
                </div>
                {/* content */}
                {section == 0 ? (<SummarySection Sections={Sections}></SummarySection>) : (<VoxGPTSection id={id}/>)}
                
                      
            </div>
            
        </main>
    )
}