# Activity 7: What-If Incident Simulations (inference only — do not refit)

# Scenario A: BD accident cleared, traffic back to normal
# Scenario B: sudden blockage on FG
whatif = pd.DataFrame([
    dict(scenario='A_BD_cleared', time_step=35, road_segment_id='BD',
         rho_current=50, rho_past=50, rho_estimated=50.0,
         active_event='None', trip_time_minutes=5.20),
    dict(scenario='B_FG_blockage', time_step=35, road_segment_id='FG',
         rho_current=190, rho_past=40, rho_estimated=130.0,
         active_event='Accident', trip_time_minutes=5.20),
])

whatif['LogReg_Predicted_Code'] = logreg_pipeline.predict(whatif[feature_cols])
whatif['LogReg_Predicted_Route'] = whatif['LogReg_Predicted_Code'].map({0: 'Route_1', 1: 'Route_2'})

print(whatif[['scenario', 'road_segment_id', 'active_event', 'rho_current', 'LogReg_Predicted_Route']])
whatif.to_csv('4_WhatIf_Inference.csv', index=False)
print("Exported: '4_WhatIf_Inference.csv'")
