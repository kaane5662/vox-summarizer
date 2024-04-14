"use client"

import axios from "axios"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function Generate(){
    const router = useRouter()
    const [url, setUrl] = useState()
    const [generating, setGenerating] = useState(false)

    const generateSummary = ()=>{
        console.log(url)
        setGenerating(true)
        axios.post(`http://localhost:5000/generate`,{url}).then((response)=>{
            router.push(`/summary/${response.data.article_id}`)
        }).catch((error)=>{
            setGenerating(false)
            console.log(error.message)
        })
        
    }

    return(
        <main className="h-screen bg-primary text-secondary flex justify-center font-cabin">
            <div className="flex items-center justify-center flex-col gap-8 w-[60%]">
                <h1 className="text-5xl font-bold">Generate Vox Summary</h1>
                <h3 className="text-xl text-center">Use our AI to seamlessly condense lengthy Vox articles into succinct summaries, providing you with essential information at a glance.</h3>
                <div className="flex w-[100%] gap-4">
                    <input onChange={(e:InputEvent)=>setUrl(e.target?.value)} className="w-[80%] text-md p-4 rounded-xl" placeholder="Input your URL here"></input>
                    <button  disabled={generating} onClick={generateSummary} className="w-[20%] disabled:bg-opacity-30 font-bold bg-complementary rounded-xl hover:scale-105 duration-300">Generate</button>
                </div>

            </div>
            
        </main>
    )
}