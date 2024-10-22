import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define functions
def fuzzy_membership(value, min_value, max_value):
    """Calculate the fuzzy membership."""
    return (max_value - value) / (max_value - min_value), (value - min_value) / (max_value - min_value)

def crisp_value(min_value, max_value, min_membership, z_formula='decrease'):
    """Calculate the crisp value (z)."""
    if z_formula == 'decrease':
        return max_value - min_membership * (max_value - min_value)
    elif z_formula == 'increase':
        return min_value + min_membership * (max_value - min_value)

def fuzzy_tsukamoto(min_demand, max_demand, min_stock, max_stock, min_production, max_production, demand, stock):
    # Calculate memberships
    mu_demand_down, mu_demand_up = fuzzy_membership(demand, min_demand, max_demand)
    mu_stock_down, mu_stock_up = fuzzy_membership(stock, min_stock, max_stock)

    # RULE 1
    min_rule1 = min(mu_demand_down, mu_stock_up)
    Z1 = crisp_value(min_production, max_production, min_rule1, 'decrease')

    # RULE 2
    min_rule2 = min(mu_demand_down, mu_stock_down)
    Z2 = crisp_value(min_production, max_production, min_rule2, 'decrease')

    # RULE 3
    min_rule3 = min(mu_demand_up, mu_stock_up)
    Z3 = crisp_value(min_production, max_production, min_rule3, 'increase')

    # RULE 4
    min_rule4 = min(mu_demand_up, mu_stock_down)
    Z4 = crisp_value(min_production, max_production, min_rule4, 'increase')

    # Calculate the final production
    final_production = (
        (min_rule1 * Z1 + min_rule2 * Z2 + min_rule3 * Z3 + min_rule4 * Z4) /
        (min_rule1 + min_rule2 + min_rule3 + min_rule4)
    )

    return final_production, mu_demand_down, mu_demand_up, mu_stock_down, mu_stock_up, Z1, Z2, Z3, Z4

# Streamlit UI
st.title("Fuzzy Tsukamoto Production System")

# Input section
st.header("Input Parameters")
min_demand = st.number_input("Permintaan minimum", min_value=0)
max_demand = st.number_input("Permintaan maksimum", min_value=0)
min_stock = st.number_input("Stok minimum", min_value=0)
max_stock = st.number_input("Stok maksimum", min_value=0)
min_production = st.number_input("Produksi minimum", min_value=0)
max_production = st.number_input("Produksi maksimum", min_value=0)
demand = st.number_input("Jumlah permintaan", min_value=0)
stock = st.number_input("Jumlah stok", min_value=0)

# Perform calculation when button is clicked
if st.button("Hitung Produksi"):
    final_production, mu_demand_down, mu_demand_up, mu_stock_down, mu_stock_up, Z1, Z2, Z3, Z4 = fuzzy_tsukamoto(
        min_demand, max_demand, min_stock, max_stock, min_production, max_production, demand, stock
    )
    
    # Display results
    st.subheader("Hasil")
    st.write(f"Produksi yang harus dilakukan: {final_production}")
    st.write(f"μ Permintaan Turun: {mu_demand_down}")
    st.write(f"μ Permintaan Naik: {mu_demand_up}")
    st.write(f"μ Stok Sedikit: {mu_stock_down}")
    st.write(f"μ Stok Banyak: {mu_stock_up}")
    st.write(f"Z1: {Z1}, Z2: {Z2}, Z3: {Z3}, Z4: {Z4}")

    # Plot demand graph
    st.subheader("Grafik Permintaan")
    x = np.linspace(min_demand, max_demand, 500)
    y_turun = np.clip(1 - (x - min_demand) / (max_demand - min_demand), 0, 1)  # Decreasing from 1 to 0
    y_naik = np.clip((x - min_demand) / (max_demand - min_demand), 0, 1)        # Increasing from 0 to 1

    fig, ax = plt.subplots()
    ax.plot(x, y_turun, color='black', linewidth=1.5, label="Turun")
    ax.plot(x, y_naik, color='black', linewidth=1.5, label="Naik")
    ax.vlines([min_demand, max_demand], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.set_xlabel("Permintaan (kemasan/hari)")
    ax.set_ylabel("$\mu[x]$")
    st.pyplot(fig)

    # Plot stock graph
    st.subheader("Grafik Stok")
    x = np.linspace(min_stock, max_stock, 500)
    y_turun = np.clip(1 - (x - min_stock) / (max_stock - min_stock), 0, 1)  # Decreasing from 1 to 0
    y_naik = np.clip((x - min_stock) / (max_stock - min_stock), 0, 1)        # Increasing from 0 to 1

    fig, ax = plt.subplots()
    ax.plot(x, y_turun, color='black', linewidth=1.5, label="Turun")
    ax.plot(x, y_naik, color='black', linewidth=1.5, label="Naik")
    ax.vlines([min_stock, max_stock], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.set_xlabel("Stok (kemasan/hari)")
    ax.set_ylabel("$\mu[x]$")
    st.pyplot(fig)

    # Plot production graph
    st.subheader("Grafik Produksi")
    x = np.linspace(min_production, max_production, 500)
    y_turun = np.clip(1 - (x - min_production) / (max_production - min_production), 0, 1)  # Decreasing from 1 to 0
    y_naik = np.clip((x - min_production) / (max_production - min_production), 0, 1)        # Increasing from 0 to 1

    fig, ax = plt.subplots()
    ax.plot(x, y_turun, color='black', linewidth=1.5, label="Turun")
    ax.plot(x, y_naik, color='black', linewidth=1.5, label="Naik")
    ax.vlines([min_production, max_production], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.set_xlabel("Produksi (unit/hari)")
    ax.set_ylabel("$\mu[x]$")
    st.pyplot(fig)
