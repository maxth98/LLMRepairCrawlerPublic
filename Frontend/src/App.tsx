import mapboxgl from 'mapbox-gl'
import './App.css'
import LLMMap from './components/map'
import { datasetType } from './api/api';
import keysJson from '../../Backend/data/tokens.json'; 

mapboxgl.accessToken = keysJson.mapbox_pb;



function App() {

  return (
    <>
    <div className='bg-transparent'>
      <LLMMap
        dataset={datasetType}
        lat={47.076668}
        lng={15.421371}
        zoomLevel={12}
      />
    </div>
    </>
  )
}

export default App
