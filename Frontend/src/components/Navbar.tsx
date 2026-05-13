import { NavLink } from "react-router";


export default function Navbar() {
    return (
        <nav className="bg-gray-800 p-4">
            <NavLink to="/">Home</NavLink>
            <NavLink to="/about">About</NavLink>
        </nav>
    )
}