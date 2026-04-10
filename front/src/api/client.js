import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export async function fetchServers(params) {
  const { data } = await api.get('/servers/', { params });
  return data;
}

export async function fetchServer(id) {
  const { data } = await api.get(`/servers/${id}/`);
  return data;
}

export async function fetchFilters() {
  const { data } = await api.get('/filters/');
  return data;
}
