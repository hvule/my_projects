import numpy as np
import matplotlib.pyplot as plt

#num_simulations = 10000
num_simulations = 10000
simulated_option_values = [] # To store the results of each simulation

# Pre-calculate PV of R&D costs at each decision point (these are fixed per simulation)
# ... (e.g., pv_phase3_costs_y5, pv_phase2_costs_y3, pv_preclinical_costs_y0)

# Define fixed PoS and risk-free rate
pos_ph3_to_approval = 0.55
pos_ph2_to_ph3 = 0.25
pos_ph1_to_ph2 = 0.40
pos_pre_to_ph1 = 0.65
risk_free_rate = 0.05 # 5%

# --- Fixed R&D and Regulatory Costs (in millions $) ---
# Phase 3 costs (Years 6, 7, 8)
r_and_d_ph3_y6_M = 75.0
r_and_d_ph3_y7_M = 75.0
r_and_d_ph3_y8_M = 75.0

# Phase 2 costs (Years 4, 5)
r_and_d_ph2_y4_M = 30.0
r_and_d_ph2_y5_M = 30.0

# Phase 1 costs (Year 3)
r_and_d_ph1_y3_M = 15.0

# Pre-clinical costs (Years 1, 2)
r_and_d_preclinical_y1_M = 5.0
r_and_d_preclinical_y2_M = 5.0

# Regulatory Submission cost (Year 9)
regulatory_cost_y9_M = 10.0

pv_regulatory_cost_y9 = regulatory_cost_y9_M

pv_phase3_costs_y5 = (r_and_d_ph3_y6_M / (1 + risk_free_rate)**1) + \
                     (r_and_d_ph3_y7_M / (1 + risk_free_rate)**2) + \
                     (r_and_d_ph3_y8_M / (1 + risk_free_rate)**3)

pv_phase2_costs_y3 = (r_and_d_ph2_y4_M / (1 + risk_free_rate)**1) + \
                     (r_and_d_ph2_y5_M / (1 + risk_free_rate)**2)

pv_preclinical_phase1_costs_y0 = (r_and_d_preclinical_y1_M / (1 + risk_free_rate)**1) + \
                                 (r_and_d_preclinical_y2_M / (1 + risk_free_rate)**2) + \
                                 (r_and_d_ph1_y3_M / (1 + risk_free_rate)**3)

# Print to verify (optional)
print(f"PV Regulatory Cost (Y9): ${pv_regulatory_cost_y9:,.2f} M")
print(f"PV Phase 3 Costs (Y5): ${pv_phase3_costs_y5:,.2f} M")
print(f"PV Phase 2 Costs (Y3): ${pv_phase2_costs_y3:,.2f} M")
print(f"PV Pre-clinical/Phase 1 Costs (Y0): ${pv_preclinical_phase1_costs_y0:,.2f} M")

def calculate_commercial_pv(sampled_peak_penetration, sampled_net_price):
    """
    Calculates the Present Value of commercial cash flows at Year 9 (launch year)
    for a given set of sampled stochastic variables.

    Args:
        sampled_peak_penetration (float): The peak market penetration rate (e.g., 0.65 for 65%)
                                         sampled for this simulation.
        sampled_net_price (float): The net price per patient (e.g., 250000)
                                 sampled for this simulation.

    Returns:
        float: The Present Value of all future commercial NOPATs discounted back to Year 9.
    """

    # --- Fixed Commercial Phase Assumptions ---
    
    target_patient_population = 50000.0 # Patients, not Millions
    cogs_rate = 0.20 # 20% of Revenue
    tax_rate = 0.25 # 25% (assumed for NOPAT calculation)
    commercial_discount_rate = 0.10 # 10%

    drug_life_post_launch_years = 15 # From Year 9 to Year 23 (15 years inclusive)

    # Market Penetration Ramp-up Logic (starting at 5% and increasing by 5% annually)
    # This ramp-up will cap at the sampled_peak_penetration.
    penetration_rates_base = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75])
    
    # SG&A Expenses Post-Launch (Year 9 to Year 23) - in millions $
  
    sga_post_launch_M = np.array([
        15.0, 20.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0
    ])

    # --- Calculation for PV of Commercial Cash Flows (at Year 9) ---
    total_pv_commercial_y9 = 0.0

    for i in range(drug_life_post_launch_years): # i = 0 for Year 9, i = 1 for Year 10, ..., i = 14 for Year 23
        year_offset = i # For discounting: current year is time 0, next year is time 1, etc.
        
        # 1. Calculate Market Penetration Rate for current year (capped by sampled peak)
        current_penetration_rate = min(penetration_rates_base[i], sampled_peak_penetration)
        
        # 2. Patients Treated
        patients_treated = target_patient_population * current_penetration_rate
        
        # 3. Total Revenue ($M)
        revenue_M = (patients_treated * sampled_net_price) / 1_000_000 # Convert to millions for consistency with SG&A
        
        # 4. Cost of Goods Sold (COGS) ($M)
        cogs_M = revenue_M * cogs_rate
        
        # 5. SG&A Expenses ($M)
        sga_M = sga_post_launch_M[i]
        
        # 6. Pre-Tax Profit ($M)
        pre_tax_profit_M = revenue_M - cogs_M - sga_M
        
        # 7. Tax ($M)
        tax_M = pre_tax_profit_M * tax_rate
        
        # 8. NOPAT ($M)
        nopat_M = pre_tax_profit_M - tax_M
        
        # Ensure NOPAT is not negative before discounting (though for these values, it should be positive)
        # NOPAT can be negative if costs exceed revenue, which is fine for the calculation.

        # 9. Discount NOPAT back to Year 9 (time 0 for commercial phase)
        # Handle the case where (1 + rate)**0 to prevent division by zero in weird scenarios
        discount_factor = (1 + commercial_discount_rate)**year_offset
        total_pv_commercial_y9 += nopat_M / discount_factor

    return total_pv_commercial_y9


for _ in range(num_simulations):
    # 1. Sample uncertain variables for THIS simulation
    sampled_peak_penetration = np.random.triangular(0.4, 0.6, 0.85) # Example values
    sampled_net_price = np.random.triangular(200000, 250000, 300000) # Example values

    # --- Start Backward Induction (Replicate Excel Logic) ---
    # (This section will be repeated in each loop, using pv_commercial_y9_this_sim)
    pv_commercial_y9_this_sim = calculate_commercial_pv(sampled_peak_penetration,sampled_net_price)
    # Value at Year 8 (from Year 9 commercial PV)
    expected_val_y9_outcome = (pos_ph3_to_approval * pv_commercial_y9_this_sim) + ((1 - pos_ph3_to_approval) * 0)
    value_at_y8 = max(0, (expected_val_y9_outcome / (1 + risk_free_rate)**1) - pv_regulatory_cost_y9) # Regulatory cost is 1 year from Y8

    # Value at Year 5 (from Year 8 value)
    expected_val_y8_outcome = (pos_ph2_to_ph3 * value_at_y8) + ((1 - pos_ph2_to_ph3) * 0)
    value_at_y5 = max(0, (expected_val_y8_outcome / (1 + risk_free_rate)**3) - pv_phase3_costs_y5) # 3 years from Y5 to Y8

    # Value at Year 3 (from Year 5 value)
    expected_val_y5_outcome = (pos_ph1_to_ph2 * value_at_y5) + ((1 - pos_ph1_to_ph2) * 0)
    value_at_y3 = max(0, (expected_val_y5_outcome / (1 + risk_free_rate)**2) - pv_phase2_costs_y3) # 2 years from Y3 to Y5

    # Value at Year 0 (from Year 3 value)
    expected_val_y3_outcome = (pos_pre_to_ph1 * value_at_y3) + ((1 - pos_pre_to_ph1) * 0)
    final_option_value_y0 = max(0, (expected_val_y3_outcome / (1 + risk_free_rate)**3) - pv_preclinical_phase1_costs_y0) # 3 years from Y0 to Y3

    simulated_option_values.append(final_option_value_y0)
    # --- End Backward Induction ---

# 4. Analyze results
simulated_option_values = np.array(simulated_option_values)

print(f"Mean Real Option Value: ${np.mean(simulated_option_values):,.2f}")
print(f"Median Real Option Value: ${np.median(simulated_option_values):,.2f}")
print(f"Standard Deviation: ${np.std(simulated_option_values):,.2f}")
print(f"Minimum Value: ${np.min(simulated_option_values):,.2f}")
print(f"Maximum Value: ${np.max(simulated_option_values):,.2f}")
print(f"5th Percentile: ${np.percentile(simulated_option_values, 5):,.2f}")
print(f"95th Percentile: ${np.percentile(simulated_option_values, 95):,.2f}")

# 5. Plot histogram
plt.hist(simulated_option_values, bins=50, edgecolor='black')
plt.title('Distribution of GenePath Real Option Value (Monte Carlo)')
plt.xlabel('Real Option Value at Year 0 ($)')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()