import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="flex justify-center items-center p-6 space-x-4">
            <Link to={'/string'}>
                <button className="text-white bg-emerald-600 hover:text-emerald-800 hover:bg-emerald-200 rounded-md p-4">string form</button>
            </Link>
            <Link to={'/form'}>
                <button className="text-white bg-purple-700 hover:text-purple-800 hover:bg-purple-200 rounded-md p-4">validation form</button>
            </Link>
        </div>
    )
}

export default Home