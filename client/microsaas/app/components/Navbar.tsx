// "use client"

import Link from "next/link";
// import { useRouter } from "next/router";
export default function Navbar(){
   
    return(
        <nav className=" absolute top-1 w-[100%] text-secondary   border-secondary font-cabin ">
            <div className="px-20 py-4 flex justify-between  top-0 fixed bg-primary z-10 w-[100%] items-center">
                <div className=" flex">
                    <h1 className="text-2xl font-bold ">Vox Summarizer</h1>

                </div>
                <div className="flex items-center gap-10">
                    <Link href={"/summaries"} className="text-md font-semibold">Summaries</Link>
                    <Link href={"/generate"} className="bg-complementary font-semibold rounded-xl px-8 py-3 text-md hover:scale-105 duration-300">Generate</Link>
                </div>
            </div>
        </nav>
    )
}