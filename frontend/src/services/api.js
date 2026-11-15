const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

let authToken = localStorage.getItem('datavision_token') || 'demo_token';

export const setAuthToken = (token) => {
  authToken = token;
  if (token) {
    localStorage.setItem('datavision_token', token);
  } else {
    localStorage.removeItem('datavision_token');
  }
};

export const getAuthToken = () => authToken;

// Realistic Demo Fallbacks for immediate offline previewing
const MOCK_PATIENTS = [
  {
    id: 1,
    patient_code: 'DV-1001',
    full_name: 'Arthur Pendelton',
    age: 62,
    gender: 'Male',
    blood_group: 'O+',
    contact_phone: '+1-555-0192',
    contact_email: 'arthur.p@example.com',
    medical_history: 'Hypertension stage 1, early microalbuminuria, former smoker.',
    created_at: new Date().toISOString(),
    latest_vitals: {
      systolic_bp: 142,
      diastolic_bp: 91,
      fasting_glucose: 112,
      bmi: 28.4,
      total_cholesterol: 218,
      smoking_status: true,
      physical_activity_hours: 1.5
    },
    latest_risks: {
      heart_disease: { score: 0.76, level: 'HIGH' },
      diabetes: { score: 0.58, level: 'MODERATE' },
      stroke: { score: 0.69, level: 'HIGH' },
      kidney_disease: { score: 0.64, level: 'MODERATE' }
    }
  },
  {
    id: 2,
    patient_code: 'DV-1002',
    full_name: 'Sarah Jenkins',
    age: 45,
    gender: 'Female',
    blood_group: 'A+',
    contact_phone: '+1-555-0143',
    contact_email: 'sarah.j@example.com',
    medical_history: 'Gestational diabetes history, metabolic syndrome, sedentary worker.',
    created_at: new Date().toISOString(),
    latest_vitals: {
      systolic_bp: 124,
      diastolic_bp: 80,
      fasting_glucose: 138,
      bmi: 31.2,
      total_cholesterol: 195,
      smoking_status: false,
      physical_activity_hours: 2.0
    },
    latest_risks: {
      heart_disease: { score: 0.38, level: 'MODERATE' },
      diabetes: { score: 0.82, level: 'CRITICAL' },
      stroke: { score: 0.31, level: 'MODERATE' },
      kidney_disease: { score: 0.71, level: 'HIGH' }
    }
  },
  {
    id: 3,
    patient_code: 'DV-1003',
    full_name: 'Carlos Rodriguez',
    age: 58,
    gender: 'Male',
    blood_group: 'B-',
    contact_phone: '+1-555-0188',
    contact_email: 'carlos.r@example.com',
    medical_history: 'Hyperlipidemia, familial history of early coronary disease.',
    created_at: new Date().toISOString(),
    latest_vitals: {
      systolic_bp: 136,
      diastolic_bp: 88,
      fasting_glucose: 104,
      bmi: 27.6,
      total_cholesterol: 248,
      smoking_status: false,
      physical_activity_hours: 2.5
    },
    latest_risks: {
      heart_disease: { score: 0.84, level: 'CRITICAL' },
      diabetes: { score: 0.45, level: 'MODERATE' },
      stroke: { score: 0.52, level: 'MODERATE' },
      kidney_disease: { score: 0.48, level: 'MODERATE' }
    }
  },
  {
    id: 4,
    patient_code: 'DV-1004',
    full_name: 'Priya Sharma',
    age: 34,
    gender: 'Female',
    blood_group: 'O-',
    contact_phone: '+1-555-0177',
    contact_email: 'priya.s@example.com',
    medical_history: 'Annual health checkup, active half-marathoner, asymptomatic.',
    created_at: new Date().toISOString(),
    latest_vitals: {
      systolic_bp: 114,
      diastolic_bp: 74,
      fasting_glucose: 88,
      bmi: 21.8,
      total_cholesterol: 172,
      smoking_status: false,
      physical_activity_hours: 5.5
    },
    latest_risks: {
      heart_disease: { score: 0.12, level: 'LOW' },
      diabetes: { score: 0.08, level: 'LOW' },
      stroke: { score: 0.09, level: 'LOW' },
      kidney_disease: { score: 0.07, level: 'LOW' }
    }
  },
  {
    id: 5,
    patient_code: 'DV-1005',
    full_name: 'David Kim',
    age: 71,
    gender: 'Male',
    blood_group: 'AB+',
    contact_phone: '+1-555-0164',
    contact_email: 'david.k@example.com',
    medical_history: 'Previous transient ischemic attack (TIA), high systolic BP.',
    created_at: new Date().toISOString(),
    latest_vitals: {
      systolic_bp: 158,
      diastolic_bp: 94,
      fasting_glucose: 122,
      bmi: 29.1,
      total_cholesterol: 228,
      smoking_status: false,
      physical_activity_hours: 1.0
    },
    latest_risks: {
      heart_disease: { score: 0.79, level: 'HIGH' },
      diabetes: { score: 0.62, level: 'HIGH' },
      stroke: { score: 0.88, level: 'CRITICAL' },
      kidney_disease: { score: 0.81, level: 'CRITICAL' }
    }
  }
];

const generateMockTimeline = (patient) => {
  const now = new Date();
  const v = patient.latest_vitals || { systolic_bp: 130, diastolic_bp: 84, fasting_glucose: 105, bmi: 26, total_cholesterol: 200 };
  return [
    {
      recorded_at: new Date(now.getTime() - 210 * 86400000).toISOString(),
      systolic_bp: v.systolic_bp + 8,
      diastolic_bp: v.diastolic_bp + 5,
      fasting_glucose: v.fasting_glucose + 6,
      bmi: v.bmi + 0.8,
      total_cholesterol: v.total_cholesterol + 12
    },
    {
      recorded_at: new Date(now.getTime() - 140 * 86400000).toISOString(),
      systolic_bp: v.systolic_bp + 4,
      diastolic_bp: v.diastolic_bp + 2,
      fasting_glucose: v.fasting_glucose + 3,
      bmi: v.bmi + 0.4,
      total_cholesterol: v.total_cholesterol + 5
    },
    {
      recorded_at: new Date(now.getTime() - 70 * 86400000).toISOString(),
      systolic_bp: v.systolic_bp + 2,
      diastolic_bp: v.diastolic_bp + 1,
      fasting_glucose: v.fasting_glucose + 1,
      bmi: v.bmi + 0.2,
      total_cholesterol: v.total_cholesterol + 2
    },
    {
      recorded_at: now.toISOString(),
      systolic_bp: v.systolic_bp,
      diastolic_bp: v.diastolic_bp,
      fasting_glucose: v.fasting_glucose,
      bmi: v.bmi,
      total_cholesterol: v.total_cholesterol
    }
  ];
};

const computeMockPrediction = (input) => {
  const age = Number(input.age) || 50;
  const sbp = Number(input.systolic_bp) || 130;
  const glucose = Number(input.fasting_glucose) || 100;
  const bmi = Number(input.bmi) || 26;
  const chol = Number(input.total_cholesterol) || 200;
  const smoking = input.smoking_status ? 1 : 0;
  const activity = Number(input.physical_activity_hours) || 2.5;

  // Heart Risk
  const heartRaw = 0.05 + 0.008 * (age - 30) + 0.004 * (sbp - 110) + 0.002 * (chol - 180) + 0.18 * smoking - 0.02 * activity;
  const heartScore = Math.max(0.05, Math.min(0.95, heartRaw));

  // Diabetes Risk
  const diabRaw = 0.04 + 0.005 * (age - 30) + 0.006 * (glucose - 90) + 0.025 * (bmi - 23) - 0.03 * activity;
  const diabScore = Math.max(0.04, Math.min(0.95, diabRaw));

  // Stroke Risk
  const strokeRaw = 0.03 + 0.01 * (age - 35) + 0.006 * (sbp - 115) + 0.15 * smoking + 0.002 * (glucose - 90);
  const strokeScore = Math.max(0.03, Math.min(0.95, strokeRaw));

  // Chronic Kidney Disease (CKD) Risk
  const kidneyRaw = 0.04 + 0.008 * (age - 35) + 0.005 * (sbp - 120) + 0.004 * (glucose - 95) + 0.018 * (bmi - 24) + 0.12 * smoking - 0.015 * activity;
  const kidneyScore = Math.max(0.04, Math.min(0.95, kidneyRaw));

  const getTier = (s) => {
    if (s < 0.25) return { level: 'LOW', color: '#10B981' };
    if (s < 0.55) return { level: 'MODERATE', color: '#F59E0B' };
    if (s < 0.75) return { level: 'HIGH', color: '#F97316' };
    return { level: 'CRITICAL', color: '#EF4444' };
  };

  const getFactors = (disease) => [
    { label: 'Systolic Blood Pressure', patient_value: sbp, baseline_value: 120, impact_score: ((sbp - 120) * 0.004).toFixed(3), is_risk_driver: sbp > 125 },
    { label: 'Fasting Blood Glucose', patient_value: glucose, baseline_value: 95, impact_score: ((glucose - 95) * 0.003).toFixed(3), is_risk_driver: glucose > 105 },
    { label: 'Body Mass Index (BMI)', patient_value: bmi, baseline_value: 23, impact_score: ((bmi - 23) * 0.012).toFixed(3), is_risk_driver: bmi > 25 },
    { label: 'Serum Cholesterol', patient_value: chol, baseline_value: 190, impact_score: ((chol - 190) * 0.002).toFixed(3), is_risk_driver: chol > 200 },
    { label: 'Physical Activity', patient_value: activity, baseline_value: 3.5, impact_score: -((activity - 1.5) * 0.02).toFixed(3), is_risk_driver: activity < 2.0 }
  ];

  const getRecs = () => {
    const r = [];
    if (sbp >= 135) r.push(`Systolic BP is elevated (${sbp} mmHg). Adopt a low-sodium DASH diet and track daily BP.`);
    if (glucose >= 115) r.push(`Fasting glucose is high (${glucose} mg/dL). Restrict refined sugars and schedule HbA1c test.`);
    if (bmi >= 27) r.push(`BMI indicates overweight status (${bmi} kg/m²). Target a progressive 5-7% weight reduction.`);
    if (smoking) r.push('Immediate tobacco cessation will reduce cardiovascular, renal & stroke hazards by up to 50%.');
    if (activity < 2.5) r.push('Increase moderate aerobic exercise to at least 150 minutes per week.');
    if (r.length === 0) r.push('Vitals are well-controlled within normal bounds. Maintain active lifestyle.');
    return r.slice(0, 4);
  };

  const risks = {
    heart_disease: {
      disease_type: 'Heart Disease',
      risk_score: heartScore,
      risk_percentage: Math.round(heartScore * 100),
      risk_level: getTier(heartScore).level,
      color: getTier(heartScore).color,
      feature_contributions: getFactors('heart'),
      clinical_recommendations: getRecs()
    },
    diabetes: {
      disease_type: 'Type-2 Diabetes',
      risk_score: diabScore,
      risk_percentage: Math.round(diabScore * 100),
      risk_level: getTier(diabScore).level,
      color: getTier(diabScore).color,
      feature_contributions: getFactors('diabetes'),
      clinical_recommendations: getRecs()
    },
    stroke: {
      disease_type: 'Stroke Probability',
      risk_score: strokeScore,
      risk_percentage: Math.round(strokeScore * 100),
      risk_level: getTier(strokeScore).level,
      color: getTier(strokeScore).color,
      feature_contributions: getFactors('stroke'),
      clinical_recommendations: getRecs()
    },
    kidney_disease: {
      disease_type: 'Kidney Disease (CKD)',
      risk_score: kidneyScore,
      risk_percentage: Math.round(kidneyScore * 100),
      risk_level: getTier(kidneyScore).level,
      color: getTier(kidneyScore).color,
      feature_contributions: getFactors('kidney'),
      clinical_recommendations: [
        'Strict BP management (< 125/80 mmHg) recommended to mitigate renal hyperfiltration injury.',
        'Screen annually for microalbuminuria and serum creatinine / eGFR decline.',
        'Adopt a kidney-protective low-sodium nutritional regimen.'
      ]
    }
  };

  const avgRisk = (heartScore + diabScore + strokeScore + kidneyScore) / 4;
  const overallHealthScore = Math.max(0, Math.min(100, Math.round((1.0 - avgRisk) * 100)));

  return {
    timestamp: new Date().toISOString(),
    overall_health_score: overallHealthScore,
    risks
  };
};

const request = async (endpoint, options = {}) => {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      setAuthToken(null);
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (err) {
    console.info(`DataVision API (${endpoint}) using demo fallback:`, err.message);
    return handleOfflineFallback(endpoint, options);
  }
};

const handleOfflineFallback = (endpoint, options) => {
  if (endpoint.startsWith('/auth/login') || endpoint.startsWith('/auth/me')) {
    return {
      access_token: 'demo_token_eleanor_vance',
      token_type: 'bearer',
      user: {
        id: 1,
        email: 'doctor@datavision.com',
        full_name: 'Dr. Eleanor Vance, MD',
        role: 'doctor',
        created_at: new Date().toISOString()
      }
    };
  }

  if (endpoint.startsWith('/patients')) {
    if (options.method === 'POST') {
      const body = JSON.parse(options.body || '{}');
      const newPt = {
        id: MOCK_PATIENTS.length + 1,
        patient_code: `DV-${1000 + MOCK_PATIENTS.length + 1}`,
        ...body,
        created_at: new Date().toISOString(),
        latest_vitals: { systolic_bp: 120, diastolic_bp: 80, fasting_glucose: 95, bmi: 24, total_cholesterol: 185 },
        latest_risks: { heart_disease: { score: 0.15, level: 'LOW' } }
      };
      MOCK_PATIENTS.unshift(newPt);
      return newPt;
    }
    return MOCK_PATIENTS;
  }

  if (endpoint.startsWith('/records/timeline')) {
    const patientId = Number(endpoint.split('/').pop());
    const pt = MOCK_PATIENTS.find(p => p.id === patientId) || MOCK_PATIENTS[0];
    return generateMockTimeline(pt);
  }

  if (endpoint.startsWith('/predict/disease-risk')) {
    const body = JSON.parse(options.body || '{}');
    return computeMockPrediction(body);
  }

  if (endpoint.startsWith('/predict/what-if')) {
    const body = JSON.parse(options.body || '{}');
    const base = computeMockPrediction(body.baseline_data || {});
    const simInput = { ...body.baseline_data, ...body.modified_params };
    const sim = computeMockPrediction(simInput);

    const deltas = {};
    for (const key of ['heart_disease', 'diabetes', 'stroke', 'kidney_disease']) {
      deltas[key] = (sim.risks[key]?.risk_percentage || 0) - (base.risks[key]?.risk_percentage || 0);
    }

    return {
      baseline_risks: base.risks,
      simulated_risks: sim.risks,
      risk_delta: deltas,
      baseline_health_score: base.overall_health_score,
      simulated_health_score: sim.overall_health_score
    };
  }

  if (endpoint.startsWith('/analytics/cohort')) {
    return {
      total_patients: MOCK_PATIENTS.length,
      total_health_records: 32,
      high_risk_patients_count: 3,
      age_groups: {
        '18-35': 1,
        '36-50': 2,
        '51-65': 1,
        '65+': 1
      },
      disease_prevalence: [
        { disease: 'Heart Disease', high_risk_cases: 2, prevalence_rate: 40.0 },
        { disease: 'Diabetes', high_risk_cases: 2, prevalence_rate: 40.0 },
        { disease: 'Stroke', high_risk_cases: 2, prevalence_rate: 40.0 },
        { disease: 'Kidney Disease (CKD)', high_risk_cases: 2, prevalence_rate: 40.0 }
      ],
      risk_distribution: {
        LOW: 1,
        MODERATE: 1,
        HIGH: 2,
        CRITICAL: 1
      }
    };
  }

  return {};
};

export const api = {
  login: async (email, password) => {
    const data = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    setAuthToken(data.access_token);
    return data;
  },
  register: (userData) => request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  getMe: () => request('/auth/me'),

  getPatients: (search = '', riskFilter = '') => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (riskFilter) params.append('risk_filter', riskFilter);
    return request(`/patients/?${params.toString()}`);
  },
  getPatientById: (id) => request(`/patients/${id}`),
  createPatient: (patientData) => request('/patients/', {
    method: 'POST',
    body: JSON.stringify(patientData),
  }),

  addHealthRecord: (recordData) => request('/records/', {
    method: 'POST',
    body: JSON.stringify(recordData),
  }),
  getTimeline: (patientId) => request(`/records/timeline/${patientId}`),

  predictDiseaseRisk: (predictionInput) => request('/predict/disease-risk', {
    method: 'POST',
    body: JSON.stringify(predictionInput),
  }),
  simulateWhatIf: (baselineData, modifiedParams) => request('/predict/what-if', {
    method: 'POST',
    body: JSON.stringify({
      baseline_data: baselineData,
      modified_params: modifiedParams,
    }),
  }),
  getPredictionHistory: (patientId) => request(`/predict/history/${patientId}`),

  getCohortAnalytics: () => request('/analytics/cohort'),
  getPdfReportUrl: (patientId) => `${API_BASE_URL}/analytics/report/pdf/${patientId}`,
};
