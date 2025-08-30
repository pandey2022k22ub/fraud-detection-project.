'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function ApplyCouponPage() {
  const [formData, setFormData] = useState({
    coupon_code: '',
    user_email: '',
    original_amount: '',
    ip_address: '192.168.1.1',
    user_agent: '',
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setFormData(prev => ({
      ...prev,
      user_agent: navigator.userAgent
    }));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await api.post('/api/apply-coupon/', {
        ...formData,
        original_amount: parseFloat(formData.original_amount),
      });
      setResult(response.data);
    } catch (error: any) {
      setResult(error.response?.data || { message: 'An error occurred' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Fraud Shield
          </h1>
          <p className="text-gray-600">Apply your coupon securely</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">Apply Coupon</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-2">
                Email Address
              </label>
              <input
                type="email"
                required
                value={formData.user_email}
                onChange={(e) => setFormData({...formData, user_email: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 text-gray-900"
                placeholder="Enter your email"
              />
            </div>

            {/* Coupon Code Field */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-2">
                Coupon Code
              </label>
              <input
                type="text"
                required
                value={formData.coupon_code}
                onChange={(e) => setFormData({...formData, coupon_code: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 text-gray-900"
                placeholder="e.g., WELCOME20"
              />
            </div>

            {/* Amount Field */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-2">
                Order Amount (₹)
              </label>
              <input
                type="number"
                required
                value={formData.original_amount}
                onChange={(e) => setFormData({...formData, original_amount: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 text-gray-900"
                placeholder="1000.00"
                step="0.01"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:transform-none disabled:cursor-not-allowed shadow-md"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </span>
              ) : (
                'Apply Coupon & Check Fraud'
              )}
            </button>
          </form>

          {/* Result Display */}
          {result && (
            <div className={`mt-8 p-6 rounded-xl border-2 ${
              result.success 
                ? 'bg-green-50 border-green-200 text-green-800' 
                : 'bg-red-50 border-red-200 text-red-800'
            }`}>
              <div className="flex items-center mb-3">
                <div className={`p-2 rounded-full ${
                  result.success ? 'bg-green-100' : 'bg-red-100'
                }`}>
                  {result.success ? (
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
                <h3 className="text-lg font-semibold ml-3">
                  {result.success ? '✅ Success!' : '❌ Fraud Detected!'}
                </h3>
              </div>
              
              <p className="mb-3">{result.message}</p>
              
              {result.discounted_amount && (
                <p className="font-medium">
                  Discounted Amount: <span className="text-green-600">₹{result.discounted_amount}</span>
                </p>
              )}
              
              {result.fraud_probability !== undefined && (
                <div className="mt-4">
                  <p className="font-medium mb-2">Fraud Probability:</p>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div 
                      className={`h-2.5 rounded-full ${
                        result.fraud_probability > 0.7 ? 'bg-red-600' : 
                        result.fraud_probability > 0.4 ? 'bg-yellow-500' : 'bg-green-600'
                      }`}
                      style={{ width: `${result.fraud_probability * 100}%` }}
                    ></div>
                  </div>
                  <p className="text-sm mt-1 text-gray-600">
                    {(result.fraud_probability * 100).toFixed(2)}% risk
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Note */}
        <div className="text-center mt-8">
          <p className="text-sm text-gray-500">
            Powered by AI Fraud Detection System
          </p>
        </div>
      </div>
    </div>
  );
}