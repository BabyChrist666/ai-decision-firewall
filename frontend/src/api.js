const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Check AI output through the firewall
 * @param {Object} request - Firewall request
 * @param {string} request.ai_output - The AI-generated output
 * @param {number} request.confidence - Confidence score (0-1)
 * @param {string} request.intended_action - Action type (answer, trade, execute_code)
 * @param {string[]} request.sources - Array of source URLs
 * @returns {Promise<Object>} Firewall response
 */
export async function checkFirewall(request) {
  try {
    const response = await fetch(`${API_BASE_URL}/firewall/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ai_output: request.ai_output,
        confidence: request.confidence,
        intended_action: request.intended_action,
        sources: request.sources || [],
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Firewall check error:', error);
    throw error;
  }
}

/**
 * Get firewall metrics
 * @returns {Promise<Object>} Metrics data
 */
export async function getMetrics() {
  try {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Metrics fetch error:', error);
    throw error;
  }
}




