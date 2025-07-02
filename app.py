import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

# --- CONFIG ---
SUPABASE_URL = "https://akipfqumpvpsjjufweht.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFraXBmcXVtcHZwc2pqdWZ3ZWh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkxMDc2NzQsImV4cCI6MjA2NDY4MzY3NH0.qpFDz3WWL1H6KT5IiBOC4O1aqd6GIpZluDsc0hIrR2A"
SUPABASE_TABLE = "inventory"

# --- INIT SUPABASE ---
@st.cache_resource(show_spinner=False)
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase: Client = get_supabase()

# --- AUTH ---
def signup(username, password):
    return supabase.auth.sign_up({"email": username, "password": password})

def login(username, password):
    return supabase.auth.sign_in_with_password({"email": username, "password": password})

def logout():
    supabase.auth.sign_out()

# --- UI: Sign up / Login ---
if "user" not in st.session_state:
    st.session_state.user = None

auth_mode = st.sidebar.radio("Account", ["Login", "Sign Up"])

if not st.session_state.user:
    st.title("🔐 IT Asset Inventory - Login/Sign Up")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if auth_mode == "Sign Up":
        if st.button("Sign Up"):
            res = signup(username, password)
            if res.user:
                st.success("Account created. You can now log in.")
            else:
                st.error(res)
    else:
        if st.button("Login"):
            res = login(username, password)
            if res.user:
                st.session_state.user = res.user
                st.experimental_rerun()
            else:
                st.error("Login failed. Check credentials.")

if st.session_state.user:
    st.sidebar.write(f"Logged in as: {st.session_state.user.email}")
    if st.sidebar.button("Logout"):
        logout()
        st.session_state.user = None
        st.experimental_rerun()

    st.title("📦 IT Asset Inventory System")

    menu = ["View Inventory", "Add Asset", "Edit/Delete Asset"]
    choice = st.sidebar.selectbox("Menu", menu)

    # --- Load data ---
    @st.cache_data(show_spinner=False)
    def fetch_inventory():
        res = supabase.table(SUPABASE_TABLE).select("*").execute()
        if res.data:
            return pd.DataFrame(res.data)
        else:
            return pd.DataFrame(columns=[
                "username", "location", "status", "item", "computer name", "ip address", "mac address",
                "make", "model", "screen size", "man-serial no", "g-serial number", "operating system",
                "os version", "os build", "system type", "storage size", "memory size", "processor speed",
                "office suite", "comments", "recommendations", "date of purchase", "cost", "supplier",
                "gpo no", "warranty period", "quantity", "storage type"
            ])
    df = fetch_inventory()

    # --- View Inventory ---
    if choice == "View Inventory":
        st.subheader("Current Inventory")
        st.dataframe(df)

    # --- Add Asset ---
    elif choice == "Add Asset":
        st.subheader("Add New IT Asset")
        with st.form("asset_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                item = st.text_input("Item")
                computer_name = st.text_input("Computer Name")
                ip_address = st.text_input("IP Address")
                mac_address = st.text_input("MAC Address")
                make = st.text_input("Make")
                model = st.text_input("Model")
                screen_size = st.text_input("Screen Size")
                man_serial_no = st.text_input("Manufacturer Serial No")
                g_serial_number = st.text_input("G Serial Number")
                operating_system = st.text_input("Operating System")
                os_version = st.text_input("OS Version")
                os_build = st.text_input("OS Build")
                system_type = st.text_input("System Type")
                storage_size = st.text_input("Storage Size")
                memory_size = st.text_input("Memory Size")
                processor_speed = st.text_input("Processor Speed")
            with col2:
                office_suite = st.text_input("Office Suite")
                comments = st.text_area("Comments")
                recommendations = st.text_area("Recommendations")
                location = st.text_input("Location")
                status = st.selectbox("Status", ["Active", "Inactive", "Repair", "Disposed"])
                date_of_purchase = st.date_input("Date of Purchase")
                cost = st.text_input("Cost")
                supplier = st.text_input("Supplier")
                gpo_no = st.text_input("GPO Number")
                warranty_period = st.text_input("Warranty Period")
                quantity = st.number_input("Quantity", min_value=1, value=1)
                storage_type = st.text_input("Storage Type")
            submit = st.form_submit_button("Add Asset")

            if submit:
                asset = {
                    "username": st.session_state.user.email,
                    "location": location,
                    "status": status,
                    "item": item,
                    "computer name": computer_name,
                    "ip address": ip_address,
                    "mac address": mac_address,
                    "make": make,
                    "model": model,
                    "screen size": screen_size,
                    "man-serial no": man_serial_no,
                    "g-serial number": g_serial_number,
                    "operating system": operating_system,
                    "os version": os_version,
                    "os build": os_build,
                    "system type": system_type,
                    "storage size": storage_size,
                    "memory size": memory_size,
                    "processor speed": processor_speed,
                    "office suite": office_suite,
                    "comments": comments,
                    "recommendations": recommendations,
                    "date of purchase": str(date_of_purchase),
                    "cost": cost,
                    "supplier": supplier,
                    "gpo no": gpo_no,
                    "warranty period": warranty_period,
                    "quantity": quantity,
                    "storage type": storage_type
                }
                res = supabase.table(SUPABASE_TABLE).insert(asset).execute()
                if res.data:
                    st.success("Asset added successfully!")
                    st.cache_data.clear()
                else:
                    st.error("Failed to add asset.")

    # --- Edit/Delete Asset ---
    elif choice == "Edit/Delete Asset":
        st.subheader("Edit or Delete Asset")
        if df.empty:
            st.info("No assets to edit or delete.")
        else:
            df_user = df[df["username"] == st.session_state.user.email]
            selected_idx = st.selectbox("Select Asset (by Index)", df_user.index)
            asset = df_user.loc[selected_idx]
            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                with col1:
                    item = st.text_input("Item", asset["item"])
                    computer_name = st.text_input("Computer Name", asset["computer name"])
                    ip_address = st.text_input("IP Address", asset["ip address"])
                    mac_address = st.text_input("MAC Address", asset["mac address"])
                    make = st.text_input("Make", asset["make"])
                    model = st.text_input("Model", asset["model"])
                    screen_size = st.text_input("Screen Size", asset["screen size"])
                    man_serial_no = st.text_input("Manufacturer Serial No", asset["man-serial no"])
                    g_serial_number = st.text_input("G Serial Number", asset["g-serial number"])
                    operating_system = st.text_input("Operating System", asset["operating system"])
                    os_version = st.text_input("OS Version", asset["os version"])
                    os_build = st.text_input("OS Build", asset["os build"])
                    system_type = st.text_input("System Type", asset["system type"])
                    storage_size = st.text_input("Storage Size", asset["storage size"])
                    memory_size = st.text_input("Memory Size", asset["memory size"])
                    processor_speed = st.text_input("Processor Speed", asset["processor speed"])
                with col2:
                    office_suite = st.text_input("Office Suite", asset["office suite"])
                    comments = st.text_area("Comments", asset["comments"])
                    recommendations = st.text_area("Recommendations", asset["recommendations"])
                    location = st.text_input("Location", asset["location"])
                    status = st.selectbox("Status", ["Active", "Inactive", "Repair", "Disposed"], index=["Active", "Inactive", "Repair", "Disposed"].index(asset["status"]))
                    date_of_purchase = st.date_input("Date of Purchase", pd.to_datetime(asset["date of purchase"]))
                    cost = st.text_input("Cost", asset["cost"])
                    supplier = st.text_input("Supplier", asset["supplier"])
                    gpo_no = st.text_input("GPO Number", asset["gpo no"])
                    warranty_period = st.text_input("Warranty Period", asset["warranty period"])
                    quantity = st.number_input("Quantity", min_value=1, value=int(asset["quantity"]))
                    storage_type = st.text_input("Storage Type", asset["storage type"])
                update = st.form_submit_button("Update Asset")
                delete = st.form_submit_button("Delete Asset")

                row_id = asset["id"] if "id" in asset else asset.name  # or use your PK

                if update:
                    updated_asset = {
                        "username": st.session_state.user.email,
                        "location": location,
                        "status": status,
                        "item": item,
                        "computer name": computer_name,
                        "ip address": ip_address,
                        "mac address": mac_address,
                        "make": make,
                        "model": model,
                        "screen size": screen_size,
                        "man-serial no": man_serial_no,
                        "g-serial number": g_serial_number,
                        "operating system": operating_system,
                        "os version": os_version,
                        "os build": os_build,
                        "system type": system_type,
                        "storage size": storage_size,
                        "memory size": memory_size,
                        "processor speed": processor_speed,
                        "office suite": office_suite,
                        "comments": comments,
                        "recommendations": recommendations,
                        "date of purchase": str(date_of_purchase),
                        "cost": cost,
                        "supplier": supplier,
                        "gpo no": gpo_no,
                        "warranty period": warranty_period,
                        "quantity": quantity,
                        "storage type": storage_type
                    }
                    # Update using PK (assuming id or your primary key)
                    res = supabase.table(SUPABASE_TABLE).update(updated_asset).eq("id", row_id).execute()
                    if res.data:
                        st.success("Asset updated!")
                        st.cache_data.clear()
                    else:
                        st.error("Failed to update asset.")

                if delete:
                    res = supabase.table(SUPABASE_TABLE).delete().eq("id", row_id).execute()
                    if res.data:
                        st.warning("Asset deleted.")
                        st.cache_data.clear()
                    else:
                        st.error("Failed to delete asset.")


