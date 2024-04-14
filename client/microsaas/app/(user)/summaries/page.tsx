"use client"
import SummaryHeader from "@/app/components/SummaryHeader"
import { useEffect, useState } from "react"
import { Summary } from "@/app/types"
import axios from "axios"

// async function fetchSummaries() {
//     console.log(process.env.SERVER_DOMAIN)
//     const Summaries = await fetch(`http://localhost:5000/summaries`, {cache: "no-store"})
//     // console.log(Summaries.json())
//     return Summaries.json()
// }


export default function Summaries(){
    const [Summaries, setSummaries] = useState<Summary[]>()
    const fetchSummaries = ()=>{
        console.log(process.env.SERVER_DOMAIN)
        axios.get(`http://localhost:5000/summaries`).then((response)=>{
            setSummaries(response.data)
        }).catch((error)=>{
            console.log(error.message)
        })
    }

    useEffect(()=>{
        fetchSummaries()
    },[])
    
    return(
        <main className="min-h-screen bg-primary text-secondary flex justify-center font-cabin">
            <div className="flex py-24 flex-col gap-8 w-[60%]">
                <h1 className="text-4xl font-bold border-b-2 p-4 border-opacity-20 border-secondary">Summaries</h1>
                <div className="grid gap-8 grid-cols-3 w-[100%]">
                    {Summaries?.map((summary,index)=>{
                        return(
                            <SummaryHeader summary={summary}></SummaryHeader>
                        )
                    })}
                    {/* <SummaryHeader></SummaryHeader>
                    <SummaryHeader></SummaryHeader>
                    <SummaryHeader></SummaryHeader> */}
                </div>

            </div>
            
        </main>
    )
}