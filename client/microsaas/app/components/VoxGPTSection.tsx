import { FormEvent, useRef, useState } from "react"
import axios from "axios"
import { useRouter } from "next/navigation"
import { ChatBubble } from "../types"

export default function VoxGPTSection({id}){
    const [Bubbles, setBubbles] = useState<ChatBubble[]>([])
    const [canChat, setCanChat] = useState(true)


    const ask_article_question = (e:any)=>{
        e.preventDefault()
        let question = e.target.question.value
        e.target.question.value = ""
        setCanChat(false)
        console.log(question)
        const userBubble = {
            author: "user",
            content: question
        }
        setBubbles(prev=>[...prev, userBubble])
        axios.post(`http://localhost:5000/ask/${id}`,{question}).then((response)=>{
            const aiBubble = {
                author: "ai",
                content: response.data
            }
            setBubbles(prev=>[...prev, aiBubble])
            setCanChat(true)
        }).catch((error)=>{
            console.log(error.message)
        })
    }

    return(
        <div className="flex flex-col gap-8 ">
            {/* bubbles */}
            <div className="flex flex-col gap-8 overflow-y-scroll p-4 h-[400px]">

                {Bubbles?.map((bubble, index)=>{
                    return(

                        bubble.author == "user"?
                        <p className="p-3 rounded-2xl rounded-br-none self-end bg-complementary max-w-[40%] font-semibold text-sm">{bubble.content}</p>:
                        <p className="p-3 rounded-2xl rounded-tl-none text-left bg-white bg-opacity-60 max-w-[40%] font-semibold text-sm">{bubble.content}</p> 
                    )

                })}
            </div>
            {/* input */}

            <form onSubmit={ask_article_question} className="relative">
                <input name="question" placeholder="Ask a question about the article..." className="w-[100%] pr-32 bg-white bg-opacity-50 p-4 rounded-xl border-2 text-sm font-semibold "></input>
                <button type="submit" disabled={!canChat} className="absolute top-0 bottom-0 right-5 h-fit self-center bg-complementary rounded-xl p-2 px-5 text-sm font-bold hover:scale-105 duration-300 disabled:bg-opacity-30 ">Submit</button>
            </form>

        </div>
    )
}