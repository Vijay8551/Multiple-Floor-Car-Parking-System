import streamlit as st

# 🚗 Multi-Floor Car Parking System (Streamlit Version)

# --- Configuration ---
FLOORS = 5
SLOTS_PER_FLOOR = 20

# --- Initialize Parking (using session state) ---
if "parking" not in st.session_state:
    st.session_state.parking = [
        [str(f + 1) + str(s + 1) for s in range(SLOTS_PER_FLOOR)]
        for f in range(FLOORS)
    ]

# --- Helper Functions ---
def get_parking_stats():
    """Calculate parking statistics."""
    total_slots = FLOORS * SLOTS_PER_FLOOR
    occupied = sum(1 for floor in st.session_state.parking for slot in floor if slot == "X")
    available = total_slots - occupied
    return total_slots, occupied, available

def display_parking():
    """Display parking slots with enhanced visual design."""
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .parking-floor {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .slot-available {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1a1a1a;
        border: 2px solid #4ade80;
        border-radius: 10px;
        padding: 0.5rem;
        font-weight: bold;
        text-align: center;
        transition: all 0.3s ease;
    }
    .slot-occupied {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 0.5rem;
        font-weight: bold;
        text-align: center;
    }
    .floor-header {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display statistics
    total, occupied, available = get_parking_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Total Floors", FLOORS)
    with col2:
        st.metric("🅿️ Total Slots", total)
    with col3:
        st.metric("✅ Available", available, delta=None)
    with col4:
        st.metric("❌ Occupied", occupied, delta=None)
    
    st.markdown("---")
    st.subheader("🚘 Current Parking Status")
    
    # Display each floor with enhanced design
    for f, slots in enumerate(st.session_state.parking):
        # Floor header with custom styling
        floor_num = f + 1
        occupied_count = sum(1 for slot in slots if slot == "X")
        available_count = len(slots) - occupied_count
        
        # Create a container for each floor
        with st.container():
            # Floor header with gradient background
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1rem; 
                            border-radius: 10px; 
                            margin-bottom: 1rem;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h3 style='color: white; margin: 0; font-size: 1.5rem;'>🏢 Floor {floor_num}</h3>
                        <div style='display: flex; gap: 1rem;'>
                            <div style='background: #10b981; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;'>
                                ✅ Available: {available_count}
                            </div>
                            <div style='background: #ef4444; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;'>
                                ❌ Occupied: {occupied_count}
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Parking slots in a grid
            # Display slots in rows of 5 for better visibility
            slots_per_row = 5
            for row in range(0, len(slots), slots_per_row):
                row_slots = slots[row:row + slots_per_row]
                cols = st.columns(len(row_slots))
                
                for i, col in enumerate(cols):
                    with col:
                        slot_idx = row + i
                        slot_label = slots[slot_idx]
                        
                        if slot_label == "X":
                            # Occupied slot
                            st.markdown(
                                f"<div class='slot-occupied' style='padding: 1rem; margin: 0.3rem 0;'>"
                                f"🚗<br><strong>Occupied</strong><br>F{floor_num}-S{slot_idx + 1}"
                                f"</div>",
                                unsafe_allow_html=True
                            )
                        else:
                            # Available slot
                            st.markdown(
                                f"<div class='slot-available' style='padding: 1rem; margin: 0.3rem 0;'>"
                                f"🅿️<br><strong>F{floor_num}-S{slot_idx + 1}</strong><br>Available"
                                f"</div>",
                                unsafe_allow_html=True
                            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")


def park_car(floor, slot):
    """Park a car in the given floor and slot."""
    if st.session_state.parking[floor - 1][slot - 1] == "X":
        st.error("That slot is already occupied!")
    else:
        st.session_state.parking[floor - 1][slot - 1] = "X"
        st.success(f"✅ Car parked at Floor {floor}, Slot {slot}")
        st.rerun()  # Force immediate refresh to show updated parking status


def remove_car(floor, slot):
    """Remove a parked car from the given floor and slot."""
    if st.session_state.parking[floor - 1][slot - 1] == "X":
        st.session_state.parking[floor - 1][slot - 1] = str(floor) + str(slot)
        st.success(f"🟩 Car removed from Floor {floor}, Slot {slot}")
        st.rerun()  # Force immediate refresh to show updated parking status
    else:
        st.warning("That slot is already empty!")


# --- Streamlit Page Layout ---
st.set_page_config(
    page_title="🚗 Multi-Floor Parking System", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for overall page styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .action-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <h1>🏢 Multi-Floor Car Parking System</h1>
        <p style='font-size: 1.2rem; margin-top: 0.5rem;'>Smart Parking Management Solution</p>
    </div>
    """, unsafe_allow_html=True)

# --- User Actions (Process first, then display) ---
st.markdown("## ⚙️ Parking Actions")

tab1, tab2, tab3 = st.tabs(["🅿️ Park a Car", "🚗 Remove a Car", "📊 Quick Stats"])

with tab1:
    st.markdown("### 🅿️ Park Your Vehicle")
    st.markdown("Select the floor and slot where you want to park your car.")
    
    col1, col2 = st.columns(2)
    with col1:
        floor = st.number_input(
            "Select Floor:", 
            min_value=1, 
            max_value=FLOORS, 
            step=1,
            help=f"Choose a floor from 1 to {FLOORS}"
        )
    with col2:
        slot = st.number_input(
            "Select Slot:", 
            min_value=1, 
            max_value=SLOTS_PER_FLOOR, 
            step=1,
            help=f"Choose a slot from 1 to {SLOTS_PER_FLOOR}"
        )
    
    # Show current status of selected slot
    if floor and slot:
        current_status = st.session_state.parking[floor - 1][slot - 1]
        if current_status == "X":
            st.warning(f"⚠️ Floor {floor}, Slot {slot} is currently **OCCUPIED**")
        else:
            st.info(f"ℹ️ Floor {floor}, Slot {slot} is currently **AVAILABLE**")
    
    if st.button("🚗 Park Car Here", use_container_width=True, type="primary"):
        park_car(floor, slot)

with tab2:
    st.markdown("### 🚗 Remove Your Vehicle")
    st.markdown("Select the floor and slot from where you want to remove your car.")
    
    col1, col2 = st.columns(2)
    with col1:
        rem_floor = st.number_input(
            "Select Floor to Remove:", 
            min_value=1, 
            max_value=FLOORS, 
            step=1, 
            key="rem_floor",
            help=f"Choose a floor from 1 to {FLOORS}"
        )
    with col2:
        rem_slot = st.number_input(
            "Select Slot to Remove:", 
            min_value=1, 
            max_value=SLOTS_PER_FLOOR, 
            step=1, 
            key="rem_slot",
            help=f"Choose a slot from 1 to {SLOTS_PER_FLOOR}"
        )
    
    # Show current status of selected slot
    if rem_floor and rem_slot:
        current_status = st.session_state.parking[rem_floor - 1][rem_slot - 1]
        if current_status == "X":
            st.info(f"ℹ️ Floor {rem_floor}, Slot {rem_slot} is currently **OCCUPIED** - Ready to remove")
        else:
            st.warning(f"⚠️ Floor {rem_floor}, Slot {rem_slot} is **EMPTY**")
    
    if st.button("🚗 Remove Car", use_container_width=True, type="primary"):
        remove_car(rem_floor, rem_slot)

with tab3:
    st.markdown("### 📊 Parking Statistics")
    total, occupied, available = get_parking_stats()
    occupancy_rate = (occupied / total * 100) if total > 0 else 0
    
    # Visual progress bar
    st.markdown(f"**Overall Occupancy Rate: {occupancy_rate:.1f}%**")
    st.progress(occupancy_rate / 100)
    
    # Floor-wise breakdown
    st.markdown("#### Floor-wise Breakdown:")
    for f in range(FLOORS):
        floor_slots = st.session_state.parking[f]
        floor_occupied = sum(1 for slot in floor_slots if slot == "X")
        floor_available = len(floor_slots) - floor_occupied
        floor_rate = (floor_occupied / len(floor_slots) * 100) if len(floor_slots) > 0 else 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f"**Floor {f + 1}**")
        with col2:
            st.progress(floor_rate / 100)
        with col3:
            st.markdown(f"{floor_occupied}/{len(floor_slots)} occupied")

# --- Reset Option ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Reset Parking System", use_container_width=True):
        st.session_state.parking = [
            [str(f + 1) + str(s + 1) for s in range(SLOTS_PER_FLOOR)]
            for f in range(FLOORS)
        ]
        st.success("✅ Parking system has been reset!")
        st.rerun()  # Force immediate refresh after reset

# --- Display current parking status (after actions are processed) ---
display_parking()