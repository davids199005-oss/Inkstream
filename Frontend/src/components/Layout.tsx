import { Outlet } from "react-router"
import Navbar from "./Navbar"

export default function Layout() {
    return (
        <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-grow">
                <Outlet />
            </main>
            <footer className="bg-gray-800 p-4">
                <p className="text-white text-center">© 2026 Inkstream. All rights reserved.</p>
            </footer>
        </div>
    )
}