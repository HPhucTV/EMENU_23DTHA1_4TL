export interface DatabaseHealth {
  status: 'connected' | 'disconnected';
  dialect: string;
  latency_ms: number;
  detail: string;
}

export interface HealthResponse {
  status: 'ok';
  service: string;
  restaurant: string;
  version: string;
  environment: string;
  timezone: string;
  utc_offset: string;
  currency: string;
  timestamp: string;
  database: DatabaseHealth;
}

export interface AreaHighlight {
  code: string;
  name: string;
  summary: string;
  capacity_hint: string;
}

export interface DishPreview {
  code: string;
  category: string;
  name: string;
  description: string;
  price_vnd: number;
  price_formatted: string;
  status: 'available' | 'out_of_stock';
}

export interface BookingRuleSummary {
  slot_step_minutes: number;
  dining_duration_minutes: number;
  hold_minutes: number;
  min_advance_hours: number;
  max_advance_days: number;
  default_deposit_percent: number;
}

export interface RestaurantOverviewResponse {
  restaurant_name: string;
  tagline: string;
  city: string;
  timezone: string;
  currency: string;
  server_time_gmt7: string;
  database: DatabaseHealth;
  areas: AreaHighlight[];
  signature_dishes: DishPreview[];
  booking_rules: BookingRuleSummary;
}
