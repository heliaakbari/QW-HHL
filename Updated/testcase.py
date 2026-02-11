from qiskit_ibm_runtime import QiskitRuntimeService
 
QiskitRuntimeService.save_account(
  token="Y_afengORmoezGQSl7ljPJ3UZwtAG6D7qRIdTWIq8Gw1", # Use the 44-character API_KEY you created and saved from the IBM Quantum Platform Home dashboard
  instance="crn:v1:bluemix:public:quantum-computing:us-east:a/0d2ac5b9c3f04daea9791d4175b6a65a:b1f1595c-44d1-46de-a635-ef174f8fd088::", # Optional
  set_as_default=True, # Optional
  overwrite=True, # Optional
)
