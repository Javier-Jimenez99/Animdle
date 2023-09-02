import SearchIcon from '@mui/icons-material/Search';
import "../../styles/SearchBar.css";
import { useEffect, useState } from "react";

function SearchBar({ inputValue, setInputValue, allResults }) {
    const [results, setResults] = useState([]);

    const handleChange = (value) => {
        setInputValue(value);

        let newResults = [];
        if (value && value.length > 0 && value !== "") {
            const inputLower = value.toLowerCase();

            allResults.forEach((title) => {
                // No se si dejar que aparezca debajo si el texto es igual al de la lista
                if (title.toLowerCase().includes(inputLower) && title.toLowerCase() !== inputLower) {
                    newResults.push(title);
                }
            });
        }
        setResults(newResults);
    };

    useEffect(() => {
        if (inputValue === "") {
            setResults([]);
        }
    }, [inputValue]);

    return (
        <div className='search-results-container'>
            <div className="search-bar-container">
                <div className="input-wrapper">
                    <SearchIcon style={{ color: "#DD675B" }} />
                    <input className="search-bar" type="text" value={inputValue} placeholder="Search for an anime..." onChange={(e) => handleChange(e.target.value)} />
                </div>
                {results && results.length > 0 &&
                    <div className="results-list">
                        {results.map((result, id) => {
                            return (
                                <div
                                    key={id}
                                    className="search-result"
                                    onClick={(e) => {
                                        setInputValue(result);
                                        handleChange(result);
                                    }}
                                >
                                    {result}
                                </div>
                            )
                        })}
                    </div>
                }
            </div>
        </div>
    )
}

export default SearchBar;