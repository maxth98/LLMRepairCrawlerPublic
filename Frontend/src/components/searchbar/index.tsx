import React, { useState, KeyboardEvent, MouseEvent, Dispatch} from 'react';
import './searchbar.css'
import { getResults } from '../../api/api';

interface SearchBarProps {
  handleData: (res: any) => void;
  setLoading: Dispatch<boolean>;
}

const SearchBar: React.FC<SearchBarProps> = ({
  handleData,
  setLoading
}) => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [previousQueries, setPreviousQueries] = useState<string[]>([]);
  const [showPreviousQueries, setShowPreviousQueries] = useState<boolean>(false);

  const updatePreviousQueries = () => {
    if(searchQuery.trim().length === 0) return;
    const newQueries = [...previousQueries, searchQuery];
    const removedDuplicatesQueries = [...new Set(newQueries)];
    setPreviousQueries(removedDuplicatesQueries); 
  }

  const handleQuery = async (query: string = searchQuery) => {
    setLoading(true);
    const results = await getResults(query);
    handleData(results);
    updatePreviousQueries();
  }

  const handleSearch = (event: MouseEvent) => {
    event.stopPropagation();
    handleQuery();
  };

  const handleSearchViaEnter = (event: KeyboardEvent) => {
    if(event.key === 'Enter') {
      handleQuery();
    }
  }

  const handlePreviousQuerySearch = (previousQueryString: string) => {
    handleQuery(previousQueryString);
    setSearchQuery(previousQueryString);
  }

  const handleInputChange = (input: string) => {
    setSearchQuery(input);
    if(input.length === 0) {
      setShowPreviousQueries(true);
    } else {
      setShowPreviousQueries(false);
    }
  }

  return (
    <div className="bg-transparent">
      <div>
        <div className="search-container bg-transparent mt-6">
          <input 
            type="text" 
            className="search-bar" 
            placeholder="Search..." 
            value={searchQuery}
            onChange={(e) => handleInputChange(e.target.value)}
            onKeyDown={(e) => handleSearchViaEnter(e)}
            onClick={(_) => setShowPreviousQueries(true)}
          />
          <div className="search-icon" onClick={handleSearch}></div>
        </div>

        {(showPreviousQueries && searchQuery.length === 0 && previousQueries.length > 0) && (
          <div className="mt-3 relative flex justify-center items-center z-50">
            <div className='flex w-2/5 justify-start opacity-80 bg-slate-300 rounded-lg px-3 py-1 backdrop-blur-md transition duration-300 ease-in-out'>
              <ul className='w-full cursor-pointer'>
                {previousQueries.map((query, index) => (
                  <li className={'w-full mb-2 border-b-2 border-black flex justify-between hover:bg-slate-100 rounded-sm'} key={index} onClick={(_) => handlePreviousQuerySearch(query)}>
                    <span className='flex text-base'>{query}</span>
                    <span className='flex'><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABYklEQVR4nN2VTUoDQRCFPxIyG83SgFcw3kG9gESRXEEM/iQeQoLHUKPnMSP+RL1EdGE2iRS8hkanpzuzzIOCYV51veqaqhpYdWRAF7gHXoFvmT2PxJlPJRwCn8AiYh/AwTKBa8C1F+AROAe2gDVZG7gAxp7fUGejcMF/gOPIIeNO5OtEomVxwXcKeJftX+x6Ip1Q8MyruWXOEgKGnrh3oFHk0PVqXqsgUAdy8UdFDg8izwIBYgKGvvi7IvJNpHVLVYG2eJuTf5iKbCYItAJ8U/y0qkAunzwgUiqQUqJWRGS7rEQjkTahZdjwJvgF2PS4S72/KWvTccLIt7ybWP+7Nn0qa9NMi2uh8SdBxPc71dlJaNDQVnSrwsY/FXvADJgD+zHnoSfS09VDqCvzmc5cpWRT80QWqnVfQ7Qus24ZeDWfK3jSunboaHHFfjiTlLKE0FBH2G6xlvySPQO34oIfdDXwC3NuhubLqYFOAAAAAElFTkSuQmCC"/></span>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        )}
      </div>
    </div>
  );
};

export default SearchBar;
