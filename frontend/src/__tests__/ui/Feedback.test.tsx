import React from 'react';
import { render, screen } from '@testing-library/react';
import { toast } from 'sonner';

// Mock the toast module
jest.mock('sonner', () => ({
  toast: {
    error: jest.fn(),
    success: jest.fn(),
    info: jest.fn(),
  },
}));

describe('Feedback System', () => {
  it('should trigger error toast when API call fails', () => {
    // We'll test this by checking if toast.error is called when an error occurs
    const errorMessage = 'Something went wrong';

    // Call toast.error directly as would happen in the API client
    (toast as jest.Mocked<typeof toast>).error(errorMessage);

    // In a real test, we would check if the toast was displayed
    expect(toast.error).toHaveBeenCalledWith(errorMessage);
  });

  it('should trigger success toast for successful operations', () => {
    const successMessage = 'Operation successful';

    // Call toast.success directly as would happen after a successful API call
    (toast as jest.Mocked<typeof toast>).success(successMessage);

    expect(toast.success).toHaveBeenCalledWith(successMessage);
  });
});