import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import fetchMock from 'jest-fetch-mock';
import App from './App';

jest.useFakeTimers();

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllTimers();
    fetch.resetMocks();
  });

  it('fetches data every minute', async () => {
    const fetchSpy = jest.spyOn(global, 'fetch').mockResolvedValue({
      json: () => Promise.resolve({ data: [] }),
    });

    render(<App />);
    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalledTimes(1);
    });

    act(() => {
      jest.advanceTimersByTime(60000);
    });
    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalledTimes(2);
    });

    fetchSpy.mockRestore();
  });

  it('renders table with data fetched from API', async () => {
    const mockedData = [
      {
        name: 'Bitcoin',
        symbol: 'BTC',
        cmc_rank: 1,
        quote: {
          USD: {
            price: 40000,
            percent_change_24h: 2.5,
          },
        },
        circulating_supply: 18743956,
        last_updated: '2024-01-31T12:34:56.000Z',
      }    ];

    fetch.mockResponseOnce(JSON.stringify({ data: mockedData }));

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('row-1')).toBeInTheDocument();
      expect(screen.getByText('Bitcoin')).toBeInTheDocument();
      expect(screen.getByText('BTC')).toBeInTheDocument();
      expect(screen.getByText('40000.00')).toBeInTheDocument();
      expect(screen.getByText('2.5000')).toBeInTheDocument();
    });
  });

});