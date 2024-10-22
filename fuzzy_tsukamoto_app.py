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

# Set page configuration and theme
st.set_page_config(
    page_title="Fuzzy Tsukamoto Production System Web App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #333333;
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #e74c3c;
        border: none;
    }
    .stButton>button:hover {
        background-color: #c0392b;
    }
    .stNumberInput>div>input {
        color: white;
        background-color: #2c3e50;
    }
    h1 {
        color: #e67e22;
        font-size: 3em;
        font-weight: bold;
    }
    h2 {
        color: #f39c12;
    }
    h3 {
        color: #f1c40f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main heading
st.title("🤖 Fuzzy Tsukamoto Production System Web App")

st.markdown("""
    <div style='text-align: left; margin-top: -15px; font-size: 14px; font-style: italic; color: #f39c12;'>
        Developed by Achmad Ardani Prasha, Clavino Ourizqi Rachmadi, Hilman Syachr Ramadhan
    </div>
    <div style='text-align: left; margin-top:  5px; font-size: 14px; font-style: italic; color: #f39c12;'>
        Introduction to Artificial Intellegence - Mercu Buana University
    </div>
    """, unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("📊 Input Parameters")
st.sidebar.write("Adjust the parameters to calculate the production")

min_demand = st.sidebar.number_input("Permintaan minimum", min_value=0, value=2000)
max_demand = st.sidebar.number_input("Permintaan maksimum", min_value=0, value=6000)
min_stock = st.sidebar.number_input("Stok minimum", min_value=0, value=200)
max_stock = st.sidebar.number_input("Stok maksimum", min_value=0, value=700)
min_production = st.sidebar.number_input("Produksi minimum", min_value=0, value=3000)
max_production = st.sidebar.number_input("Produksi maksimum", min_value=0, value=8000)
demand = st.sidebar.number_input("Jumlah permintaan", min_value=0, value=5000)
stock = st.sidebar.number_input("Jumlah stok", min_value=0, value=400)

# Calculate production when button is clicked
if st.sidebar.button("💡 Hitung Produksi"):
    final_production, mu_demand_down, mu_demand_up, mu_stock_down, mu_stock_up, Z1, Z2, Z3, Z4 = fuzzy_tsukamoto(
        min_demand, max_demand, min_stock, max_stock, min_production, max_production, demand, stock
    )

    # Display results in columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💼 Hasil Perhitungan")
        st.write(f"**Produksi yang harus dilakukan:** `{final_production:.2f}`")
        st.write(f"**μ Permintaan Turun:** `{mu_demand_down:.2f}`")
        st.write(f"**μ Permintaan Naik:** `{mu_demand_up:.2f}`")
        st.write(f"**μ Stok Sedikit:** `{mu_stock_down:.2f}`")
        st.write(f"**μ Stok Banyak:** `{mu_stock_up:.2f}`")
    
    with col2:
        st.write(f"**Z1:** `{Z1:.2f}`, **Z2:** `{Z2:.2f}`")
        st.write(f"**Z3:** `{Z3:.2f}`, **Z4:** `{Z4:.2f}`")

     # Plot demand graph
    st.subheader("📈 Grafik Permintaan")
    x = np.linspace(min_demand, max_demand, 500)
    y_turun = np.clip(1 - (x - min_demand) / (max_demand - min_demand), 0, 1)
    y_naik = np.clip((x - min_demand) / (max_demand - min_demand), 0, 1)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y_turun, color='black', linewidth=1.5)
    ax.plot(x, y_naik, color='black', linewidth=1.5)
    ax.vlines([min_demand, max_demand], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.hlines(1, xmin=0, xmax=min_demand, colors='black', linewidth=1.5)
    ax.hlines(1, xmin=max_demand, xmax=max_demand + 1000, colors='black', linewidth=1.5)
    ax.hlines(1, xmin=min_demand, xmax=max_demand, colors='black', linestyles='dotted')
    ax.hlines([mu_demand_down, mu_demand_up], xmin=0, xmax=demand, colors='black', linestyles='dotted')
    ax.plot([min_demand, min_demand], [0, mu_demand_up], linestyle='dotted', color='black')
    ax.annotate('', xy=(demand, mu_demand_down), xytext=(demand, 0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    ax.annotate('', xy=(demand, mu_demand_up), xytext=(demand, mu_demand_down),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    ax.text(demand, mu_demand_down + 0.01, f'{mu_demand_down}', ha='right', va='center', fontsize=10)
    ax.text(demand, mu_demand_up + 0.01, f'{mu_demand_up}', ha='right', va='center', fontsize=10)
    ax.text(min_demand, 1.05, 'TURUN', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(max_demand, 1.05, 'NAIK', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.arrow(0, 0, max_demand + 1000, 0, head_width=0.03, head_length=100, fc='black', ec='black', linewidth=1)
    ax.arrow(0, 0, 0, 1.1, head_width=200, head_length=0.03, fc='black', ec='black', linewidth=1)
    ax.set_xlabel('Permintaan (kemasan/hari)', fontsize=12)
    ax.set_ylabel('$\mu[x]$', fontsize=12, rotation=0, labelpad=20)
    ax.set_xlim(0, max_demand + 1000)
    ax.set_ylim(0, 1.1)
    ax.set_xticks([min_demand, (min_demand + max_demand) / 2, demand, max_demand])
    ax.set_xticklabels([f'{min_demand}', f'{(min_demand + max_demand) / 2:.0f}', f'{demand}', f'{max_demand}'])
    ax.set_yticks([0, mu_demand_down, mu_demand_up, 1])

    # Use ax.set_frame_on(False) instead of ax.box(False) to remove the frame
    ax.set_frame_on(False)

    # Display the plot
    st.pyplot(fig)

    # Plotting original chart for stock
    st.subheader("📈 Grafik Stok")
    x = np.linspace(min_stock, max_stock, 500)
    y_turun = np.clip(1 - (x - min_stock) / (max_stock - min_stock), 0, 1)
    y_naik = np.clip((x - min_stock) / (max_stock - min_stock), 0, 1)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y_turun, color='black', linewidth=1.5)
    ax.plot(x, y_naik, color='black', linewidth=1.5)
    ax.vlines([min_stock, max_stock], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.hlines(1, xmin=0, xmax=min_stock, colors='black', linewidth=1.5)
    ax.hlines(1, xmin=max_stock, xmax=max_stock + 1000, colors='black', linewidth=1.5)
    ax.hlines(1, xmin=min_stock, xmax=max_stock, colors='black', linestyles='dotted')
    ax.hlines([mu_stock_down, mu_stock_up], xmin=0, xmax=stock, colors='black', linestyles='dotted')
    ax.plot([min_stock, min_stock], [0, mu_stock_up], linestyle='dotted', color='black')
    ax.annotate('', xy=(stock, mu_stock_down), xytext=(stock, 0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    ax.annotate('', xy=(stock, mu_stock_up), xytext=(stock, mu_stock_down),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    ax.text(stock, mu_stock_down + 0.01, f'{mu_stock_down}', ha='right', va='center', fontsize=10)
    ax.text(stock, mu_stock_up + 0.01, f'{mu_stock_up}', ha='right', va='center', fontsize=10)
    ax.text(min_stock, 1.05, 'TURUN', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(max_stock, 1.05, 'NAIK', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.arrow(0, 0, max_stock + 1000, 0, head_width=0.03, head_length=100, fc='black', ec='black', linewidth=1)
    ax.arrow(0, 0, 0, 1.1, head_width=200, head_length=0.03, fc='black', ec='black', linewidth=1)
    ax.set_xlabel('Stok (kemasan/hari)', fontsize=12)
    ax.set_ylabel('$\mu[x]$', fontsize=12, rotation=0, labelpad=20)
    ax.set_xlim(0, max_stock + 1000)
    ax.set_ylim(0, 1.1)
    ax.set_xticks([min_stock, (min_stock + max_stock) / 2, stock, max_stock])
    ax.set_xticklabels([f'{min_stock}', f'{(min_stock + max_stock) / 2:.0f}', f'{stock}', f'{max_stock}'])
    ax.set_yticks([0, mu_stock_down, mu_stock_up, 1])
    ax.grid(False)
    ax.set_frame_on(False)
    st.pyplot(fig)

    # Plotting original chart for production
    st.subheader("📈 Grafik Produksi")
    x = np.linspace(min_production, max_production, 500)
    y_turun = np.clip(1 - (x - min_production) / (max_production - min_production), 0, 1)
    y_naik = np.clip((x - min_production) / (max_production - min_production), 0, 1)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y_turun, color='black', linewidth=2)
    ax.plot(x, y_naik, color='black', linewidth=2)
    ax.vlines([min_production, max_production], ymin=0, ymax=1, colors='black', linestyles='dotted')
    ax.hlines(1, xmin=0, xmax=min_production, colors='black', linewidth=2)
    ax.hlines(1, xmin=max_production, xmax=max_production + 1000, colors='black', linewidth=2)
    ax.hlines(1, xmin=min_production, xmax=max_production, colors='black', linestyles='dotted')
    ax.plot([min_production, min_production], [0, 1], linestyle='dotted', color='black')
    ax.text(min_production, 1.05, 'TURUN', ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(max_production, 1.05, 'NAIK', ha='center', va='center', fontsize=16, fontweight='bold')
    ax.arrow(0, 0, max_production + 1000, 0, head_width=0.05, head_length=100, fc='black', ec='black', linewidth=2)
    ax.arrow(0, 0, 0, 1.1, head_width=200, head_length=0.05, fc='black', ec='black', linewidth=2)
    ax.set_xlabel('Produksi (unit/hari)', fontsize=16)
    ax.set_ylabel('$\mu[x]$', fontsize=16, rotation=0, labelpad=20)
    ax.set_xlim(0, max_production + 1000)
    ax.set_ylim(0, 1.1)
    ax.set_xticks([min_production, (min_production + max_production) / 2, max_production])
    ax.set_xticklabels([f'{min_production}', f'{(min_production + max_production) / 2:.0f}', f'{max_production}'], fontsize=14)
    ax.set_yticks([0, 0.5, 1])
    ax.grid(False)
    ax.set_frame_on(False)
    st.pyplot(fig)

else:
    st.write("Set the parameters in the sidebar and click 'Hitung Produksi' to see the results.")               
