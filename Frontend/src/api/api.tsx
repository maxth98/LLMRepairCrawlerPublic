export const datasetType: string = 'apify'; // apify or osm


export const getResults = (query: string): Promise<any>  => {
  const updatedQuery = query.replaceAll(' ', '%20');

  var url = ''
  if(datasetType === 'osm') {
    url = `http://localhost:5000/answer?question=${updatedQuery}&dataset_id=styria_proc&source=osm`;
  } else {
    url = `http://localhost:5000/answer?question=${updatedQuery}&dataset_id=apify_result&source=apify`
  }

  return fetch(url).then(response => response.json());
}

export const getDataset = (dataset: string = 'osm'): Promise<any> => {
  if(dataset === 'apify') {
    return fetch('http://localhost:5000/dataset?dataset_id=apify_result&source=apify').then(response => response.json());
  }
  return fetch('http://localhost:5000/dataset?dataset_id=styria_proc&source=osm').then(response => response.json());
}