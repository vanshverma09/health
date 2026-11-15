# DataVision Health: Viva Voce & Oral Defense Preparation Guide

A comprehensive compilation of **25 high-frequency technical questions and model answers** for defending the **DataVision Health** project before university examiners and evaluation panels.

---

## 🎯 Category 1: Machine Learning & Algorithms

### Q1: Why did you choose Random Forest over Deep Neural Networks for disease risk prediction?
**Answer:**  
"For tabular clinical biomarker datasets (e.g., blood pressure, glucose, cholesterol, BMI), tree-based ensemble models like Random Forest and Gradient Boosted Trees consistently outperform deep neural networks in both accuracy and training efficiency. Furthermore, healthcare applications demand high explainability; Random Forests are less prone to overfitting on medium-sized cohorts, naturally handle non-linear feature interactions, provide intrinsic feature importance metrics, and integrate seamlessly with SHAP (Shapley Additive Explanations) without requiring massive GPU hardware."

### Q2: How did you handle class imbalance in disease prediction?
**Answer:**  
"In real-world epidemiological data, healthy patients outnumber diseased individuals. We addressed this by configuring `class_weight='balanced'` in our classifiers. This automatically adjusts weights inversely proportional to class frequencies in the input data:
$$w_j = \frac{N}{k \cdot n_j}$$
Where $N$ is total samples, $k$ is number of classes, and $n_j$ is samples in class $j$. This ensures the loss function heavily penalizes false negatives, which is critical in healthcare."

### Q3: What evaluation metrics did you prioritize, and why not just Accuracy?
**Answer:**  
"In medical screening, standard Accuracy is misleading due to class imbalance—a model predicting 'No Disease' 100% of the time could achieve 85% accuracy while missing all sick patients. Therefore, we prioritized **Sensitivity (Recall)** to minimize deadly False Negatives, along with **ROC-AUC (Area Under the Receiver Operating Characteristic Curve)**, which measures the model’s discriminatory ability across all classification thresholds."

---

## 🧠 Category 2: Explainable AI (XAI) & "Data Vision"

### Q4: What makes this project 'Data Vision' instead of just a standard prediction script?
**Answer:**  
"Traditional machine learning systems act as 'black boxes'—they output an isolated probability number with zero visual justification. 'Data Vision' transforms raw numerical data into visual clinical intelligence in three distinct dimensions:
1. **Longitudinal Biomarker Vision:** Visualizing patient physiological trajectories over time using interactive multi-series charts with color-coded clinical threshold bands.
2. **Explainable AI Attribution Vision:** Decomposing the prediction using diverging horizontal impact bars that visibly illustrate which biomarkers drive risk up (Crimson) vs. down (Emerald).
3. **Counterfactual 'What-If' Simulation:** Allowing the clinician to slide lifestyle variables and visualize immediate risk reduction deltas."

### Q5: How do your Explainable AI calculations work mathematically?
**Answer:**  
"Our attribution engine is grounded in cooperative game theory (Shapley values). For any patient biomarker $x_i$, the attribution $\phi_i$ measures the divergence between the patient's observed biomarker and an established healthy baseline median $b_i$, weighted by the ensemble feature importance $w_i$:
$$\phi_i = (x_i - b_i) \cdot w_i \cdot \kappa$$
This assigns an exact directional percentage impact to each vital sign, explaining precisely *why* the patient is categorized as Low, Moderate, High, or Critical risk."

---

## 💻 Category 3: System Architecture & Web Engineering

### Q6: Why did you choose FastAPI over Flask or Django?
**Answer:**  
"FastAPI was selected for three core technical reasons:
1. **Asynchronous Concurrency:** Built on ASGI (Starlette + Uvicorn), FastAPI handles high concurrent throughput with low memory overhead.
2. **Pydantic Data Validation:** Medical biomarker inputs are strictly validated with type enforcement and range constraints, preventing malformed telemetry.
3. **Native OpenAPI / Swagger Docs:** FastAPI automatically generates interactive documentation (`/docs`), making API testing and integration seamless."

### Q7: How is user authentication and session security maintained?
**Answer:**  
"We implemented stateless JWT (JSON Web Token) authentication using the HS256 algorithm. Passwords are never stored in plaintext; they are hashed using BCrypt with automatic salting. All sensitive patient and prediction routes are protected via FastAPI dependency injection (`get_current_user`), verifying the bearer token and enforcing role-based permissions."

### Q8: What database are you using, and what is the schema design?
**Answer:**  
"We use an enterprise relational database accessed via SQLAlchemy ORM (SQLite for zero-config demonstration, easily switchable to PostgreSQL via environment variables). The schema consists of 4 normalized relational entities:
- `users`: Clinician credentials, roles, and profiles.
- `patients`: Demographics, blood groups, and medical history.
- `health_records`: Timestamped visits containing numerical biomarkers (BP, glucose, cholesterol, BMI).
- `prediction_logs`: Disease classification logs, risk percentages, and JSON-encoded SHAP feature contribution matrices."

---

## 📊 Category 4: The 'What-If' Simulator & PDF Reports

### Q9: How does the What-If Lifestyle Simulator work under the hood?
**Answer:**  
"The client sends the patient's current baseline vitals alongside the modified slider parameters (e.g., lower SBP, lower BMI, quitting smoking) to `/api/v1/predict/what-if`. The backend runs simultaneous inference across both parameter sets through the trained ML pipelines, calculates the net shift:
$$\Delta \text{Risk} = \text{Simulated Risk} - \text{Baseline Risk}$$
and returns the risk deltas and updated overall health scores, animating the gauges in real time."

### Q10: How are the PDF medical reports generated?
**Answer:**  
"We implemented server-side document synthesis using Python's `reportlab` library. When `/api/v1/analytics/report/pdf/{id}` is queried, the server compiles the patient's demographic information, latest biomarkers against reference tables, predicted disease risks, and physician directives into a formatted PDF stream, returned directly to the browser with `application/pdf` headers."

---

## 🚀 Category 5: Limitations & Future Scope

### Q11: What are the primary limitations of your current system?
**Answer:**  
"Currently, data ingestion requires manual entry or CSV upload rather than direct automated synchronization with hospital HL7/FHIR systems. Additionally, the models currently evaluate tabular clinical biomarkers; incorporating raw radiological imaging (such as chest X-rays or retinal fundus photography) via convolutional networks is an ongoing research area."

### Q12: How would you scale this application for an entire hospital network?
**Answer:**  
"To scale for enterprise hospital deployment:
1. Migrate the database to an AWS RDS or Google Cloud SQL PostgreSQL instance with read replicas.
2. Containerize the backend and frontend using Docker and deploy on Kubernetes or AWS ECS with auto-scaling.
3. Place Redis in front of the prediction engine to cache frequently evaluated patient risk profiles.
4. Establish HL7 / FHIR API connectors to ingest vitals directly from hospital bedside monitors and lab EHR databases."

