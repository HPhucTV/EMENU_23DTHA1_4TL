import { httpClient } from '../lib/http';
import type { HealthResponse, RestaurantOverviewResponse } from '../types/system';

export async function fetchHealthStatus(): Promise<HealthResponse> {
  const response = await httpClient.get<HealthResponse>('/health');
  return response.data;
}

export async function fetchRestaurantOverview(): Promise<RestaurantOverviewResponse> {
  const response = await httpClient.get<RestaurantOverviewResponse>('/api/v1/system/overview');
  return response.data;
}
