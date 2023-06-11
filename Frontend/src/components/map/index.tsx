import React, { useEffect, useRef, useState } from 'react';
import mapboxgl, { Marker } from 'mapbox-gl';

import './map.css'
import SearchBar from '../searchbar';
import { getDataset } from '../../api/api';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Spinner = () => {
  return (
    <div className="spinner-wrapper">
      <div className="spinner"></div>
    </div>
  )
}

// Define type for the props
interface MapProps {
  dataset: string;
  lat: number; 
  lng: number;
  zoomLevel: number;
};

const LLMMap: React.FC<MapProps> = ({
  dataset,
  lat,
  lng,
  zoomLevel,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [markers, setMarkers] = useState<Record<string, Marker>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState(null);

  const createMarkers = (dataParam: any = undefined, updateMarkers: boolean = true) => {
    const allMarkers: Record<string, Marker> = {};
    const markerData = dataParam !== undefined ? dataParam : data;
    for (const [key_, value] of Object.entries(markerData)) {

      const marker = createMarker(key_, value);

      allMarkers[key_] = marker;
      
      marker.addTo(map.current!);     
    }

    if(updateMarkers) {
      setMarkers(allMarkers);
    } 
    return allMarkers;
  }
  
  const createFileAndDownload = (data: string[]) => {
    const fileContents = data.join('\n');
    const file = new Blob([fileContents], { type: 'text/plain;charset=utf-8' });
    const fileUrl = URL.createObjectURL(file);
  
    return fileUrl;
  };

  const createMarker = (key: string, value: any, color: string = '#3FB1CE'): mapboxgl.Marker => {
    var popup;

    if(dataset === 'apify') {
      var fileContentTag = ''
      if(value.content) {
        const fileName = key + '.txt';
        const fileUrl = createFileAndDownload(value.content);
        fileContentTag = `<p><b>Content: </b><a href="${fileUrl}" target="_blank" download="${fileName}">Download &#8599;</a></p>`
      }

      popup = new mapboxgl.Popup().setHTML(
        `<h2>${key}</h2>
          <p><b>Categoryname: </b>${value.categoryName}</p>
          <p><b>Phone: </b>${value.phone}</p>
          <p><b>Address: </b>${value.address}</p>
          <p><b>Website: </b><a href="${value.website}" target="_blank">${value.website}</a></p>
          ${fileContentTag}
        `
      );
    } else {
      popup = new mapboxgl.Popup().setHTML(
        `<h2>${value.name}</h2>
          <p>E-Mail: ${value.props.email !== undefined ? value.props.email : ''}</p>
          <p>Phone: ${value.props.phone !== undefined ? value.props.phone : ''}</p>
          <p>Address: ${value.props.address}</p>
          <p>Website: <a href="${value.props.website}" target="_blank">${value.props.website}</a></p>
        `
      );
    }

    return new mapboxgl.Marker({color: color}).setLngLat(value.location).setPopup(popup);
  }

  useEffect(() => {
    if(!mapContainer.current) return;

    const fetchData = async () => {
      const data = await getDataset(dataset);

      createMarkers(data.dataset);
      setLoading(false);
      setData(data.dataset);
    }

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v12?optimize=true',
      center: [lng, lat],
      zoom: zoomLevel
    });

    map.current.addControl(new mapboxgl.NavigationControl());

    fetchData()
  }, []);

  const getMapBounds = (latlngs: Array<any>) => {
    return latlngs.reduce((bounds, latlng) => {
      return bounds.extend(latlng);
    }, new mapboxgl.LngLatBounds(latlngs[0], latlngs[0]));
  }

  const handleSearchQuery = (results: any) => {
    const prevMarkers = createMarkers(undefined, false);
    if(typeof results == 'object' && Object.keys(results).length === 0) {
      setLoading(false);
      setMarkers(prevMarkers);
      toast.error(`We found no entities!`, {
        position: toast.POSITION.BOTTOM_CENTER
      });
      return;
    }

    const newMarkerLatLng = [];
    for (const [key_, value] of Object.entries(results)) {
      const color_orange = '#ED7014';
      const marker = createMarker(key_, value, color_orange);

      prevMarkers[key_] = marker;
      newMarkerLatLng.push(marker.getLngLat());
      marker.addTo(map.current!);
    }

    setMarkers(prevMarkers);

    const bounds = getMapBounds(newMarkerLatLng);

    map.current?.fitBounds(bounds, {
      padding: 150
    });

    toast.success(`We found ${Object.keys(results).length} appropriate Entities!`, {
      position: toast.POSITION.BOTTOM_CENTER
    });
    setLoading(false);
  }

  return (
    <div className='h-screen'>
      {loading && (
        <Spinner/>
      )}
      <div ref={mapContainer} className="map-container">
        <SearchBar handleData={handleSearchQuery} setLoading={setLoading}></SearchBar>
      </div>
      <ToastContainer className="z-50"/>
    </div>
  );
};

export default LLMMap;
