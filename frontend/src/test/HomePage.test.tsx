import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { formatVND } from '../lib/formatters';
import { HomePage } from '../pages/HomePage';
import * as systemApi from '../services/systemApi';

describe('US-01 Frontend Skeleton & Sample API Integration', () => {
  it('formats Vietnamese currency in VND accurately', () => {
    expect(formatVND(185000)).toContain('185.000');
    expect(formatVND(185000)).toContain('₫');
  });

  it('renders HomePage and displays data fetched from FastAPI sample endpoints', async () => {
    vi.spyOn(systemApi, 'fetchHealthStatus').mockResolvedValue({
      status: 'ok',
      service: 'emenu-backend',
      restaurant: 'Nhà hàng Ẩm thực Vườn Phố',
      version: '0.1.0',
      environment: 'test',
      timezone: 'Asia/Ho_Chi_Minh',
      utc_offset: 'GMT+7',
      currency: 'VND',
      timestamp: '2026-11-26T14:30:00+07:00',
      database: {
        status: 'connected',
        dialect: 'postgresql',
        latency_ms: 1.5,
        detail: 'Kết nối cơ sở dữ liệu sẵn sàng.',
      },
    });

    vi.spyOn(systemApi, 'fetchRestaurantOverview').mockResolvedValue({
      restaurant_name: 'Nhà hàng Ẩm thực Vườn Phố',
      tagline: 'Một chốn xanh, vạn vị thân quen.',
      city: 'TP. Hồ Chí Minh',
      timezone: 'Asia/Ho_Chi_Minh (GMT+7)',
      currency: 'VND',
      server_time_gmt7: '2026-11-26T14:30:00+07:00',
      database: {
        status: 'connected',
        dialect: 'postgresql',
        latency_ms: 1.5,
        detail: 'Kết nối cơ sở dữ liệu sẵn sàng.',
      },
      areas: [
        {
          code: 'SV',
          name: 'Sân vườn',
          summary: 'Khoáng đạt, gần gũi thiên nhiên.',
          capacity_hint: 'Bàn 2 – 8 khách',
        },
      ],
      signature_dishes: [
        {
          code: 'VP-M01',
          category: 'Món chính',
          name: 'Bò cuốn lá lốt',
          description: 'Thơm lừng lá lốt, đậm đà vị Việt.',
          price_vnd: 185000,
          price_formatted: '185.000 ₫',
          status: 'available',
        },
      ],
      booking_rules: {
        slot_step_minutes: 30,
        dining_duration_minutes: 90,
        hold_minutes: 10,
        min_advance_hours: 2,
        max_advance_days: 30,
        default_deposit_percent: 30,
      },
    });

    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter
          future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
        >
          <HomePage />
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText('FastAPI 200 OK')).toBeInTheDocument();
    expect(await screen.findByText('Bò cuốn lá lốt')).toBeInTheDocument();
    expect(await screen.findByText('Sân vườn')).toBeInTheDocument();
  });
});
