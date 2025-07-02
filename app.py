import streamlit as st
import pandas as pd
from database import init_db, SessionLocal, Asset

# --- INIT DB ---
init_db()

# --- In-memory AUTH (not secure) ---
if "user" not in st.session_state:
    st.session_state.user = None

if "users" not in st.session_state:
    st.session_state.users = {}  # {"email": "password"}

# --- AUTH ---
if not st.session_state.user:
    st.title("🔐 IT Asset Inventory - Login/Sign Up")
    auth_mode = st.sidebar.radio("Account", ["Login", "Sign Up"])
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    allowed_domain = "example.com"  # Change this to your org domain
    if auth_mode == "Sign Up":
        if st.button("Sign Up"):
            if "@" not in username or not username.endswith(f"@{allowed_domain}"):
                st.error(f"Only @{allowed_domain} emails are allowed.")
            elif username in st.session_state.users:
                st.error("User already exists.")
            else:
                st.session_state.users[username] = password
                st.success("Account created. You can now log in.")
    else:
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.user = {"email": username}
                st.experimental_rerun()
            else:
                st.error("Login failed. Check credentials.")

# --- MAIN APP ---
if st.session_state.user:
    st.sidebar.write(f"✅ Logged in as: {st.session_state.user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

    st.title("📦 IT Asset Inventory System")
    menu = ["View Inventory", "Add Asset", "Edit/Delete Asset"]
    choice = st.sidebar.selectbox("Menu", menu)

    def fetch_inventory():
        db = SessionLocal()
        assets = db.query(Asset).all()
        db.close()
        return pd.DataFrame([
            {k: v for k, v in a.__dict__.items() if k != "_sa_instance_state"}
            for a in assets
        ])

    df = fetch_inventory()

    if choice == "View Inventory":
        st.subheader("Current Inventory")
        st.dataframe(df)

    elif choice == "Add Asset":
        st.subheader("Add New IT Asset")
        with st.form("asset_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                username_input = st.text_input("Username (asset owner)")
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
                db = SessionLocal()
                asset = Asset(
                    username=username_input,
                    location=location,
                    status=status,
                    item=item,
                    computer_name=computer_name,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    make=make,
                    model=model,
                    screen_size=screen_size,
                    man_serial_no=man_serial_no,
                    g_serial_number=g_serial_number,
                    operating_system=operating_system,
                    os_version=os_version,
                    os_build=os_build,
                    system_type=system_type,
                    storage_size=storage_size,
                    memory_size=memory_size,
                    processor_speed=processor_speed,
                    office_suite=office_suite,
                    comments=comments,
                    recommendations=recommendations,
                    date_of_purchase=str(date_of_purchase),
                    cost=cost,
                    supplier=supplier,
                    gpo_no=gpo_no,
                    warranty_period=warranty_period,
                    quantity=quantity,
                    storage_type=storage_type
                )
                db.add(asset)
                db.commit()
                db.close()
                st.success("Asset added successfully!")

    elif choice == "Edit/Delete Asset":
        st.subheader("Edit or Delete Asset")
        if df.empty:
            st.info("No assets to edit or delete.")
        else:
            selected_idx = st.selectbox("Select Asset (by Index)", df.index)
            asset = df.loc[selected_idx]

            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                with col1:
                    username_input = st.text_input("Username", asset["username"])
                    item = st.text_input("Item", asset["item"])
                    computer_name = st.text_input("Computer Name", asset["computer_name"])
                    ip_address = st.text_input("IP Address", asset["ip_address"])
                    mac_address = st.text_input("MAC Address", asset["mac_address"])
                    make = st.text_input("Make", asset["make"])
                    model = st.text_input("Model", asset["model"])
                    screen_size = st.text_input("Screen Size", asset["screen_size"])
                    man_serial_no = st.text_input("Manufacturer Serial No", asset["man_serial_no"])
                    g_serial_number = st.text_input("G Serial Number", asset["g_serial_number"])
                    operating_system = st.text_input("Operating System", asset["operating_system"])
                    os_version = st.text_input("OS Version", asset["os_version"])
                    os_build = st.text_input("OS Build", asset["os_build"])
                    system_type = st.text_input("System Type", asset["system_type"])
                    storage_size = st.text_input("Storage Size", asset["storage_size"])
                    memory_size = st.text_input("Memory Size", asset["memory_size"])
                    processor_speed = st.text_input("Processor Speed", asset["processor_speed"])
                with col2:
                    office_suite = st.text_input("Office Suite", asset["office_suite"])
                    comments = st.text_area("Comments", asset["comments"])
                    recommendations = st.text_area("Recommendations", asset["recommendations"])
                    location = st.text_input("Location", asset["location"])
                    status = st.selectbox("Status", ["Active", "Inactive", "Repair", "Disposed"], index=["Active", "Inactive", "Repair", "Disposed"].index(asset["status"]))
                    date_of_purchase = st.date_input("Date of Purchase", pd.to_datetime(asset["date_of_purchase"]))
                    cost = st.text_input("Cost", asset["cost"])
                    supplier = st.text_input("Supplier", asset["supplier"])
                    gpo_no = st.text_input("GPO Number", asset["gpo_no"])
                    warranty_period = st.text_input("Warranty Period", asset["warranty_period"])
                    quantity = st.number_input("Quantity", min_value=1, value=int(asset["quantity"]))
                    storage_type = st.text_input("Storage Type", asset["storage_type"])

                update = st.form_submit_button("Update Asset")
                delete = st.form_submit_button("Delete Asset")

                row_id = asset["id"]

                if update:
                    db = SessionLocal()
                    db_asset = db.query(Asset).filter(Asset.id == row_id).first()
                    db_asset.username = username_input
                    db_asset.item = item
                    db_asset.computer_name = computer_name
                    db_asset.ip_address = ip_address
                    db_asset.mac_address = mac_address
                    db_asset.make = make
                    db_asset.model = model
                    db_asset.screen_size = screen_size
                    db_asset.man_serial_no = man_serial_no
                    db_asset.g_serial_number = g_serial_number
                    db_asset.operating_system = operating_system
                    db_asset.os_version = os_version
                    db_asset.os_build = os_build
                    db_asset.system_type = system_type
                    db_asset.storage_size = storage_size
                    db_asset.memory_size = memory_size
                    db_asset.processor_speed = processor_speed
                    db_asset.office_suite = office_suite
                    db_asset.comments = comments
                    db_asset.recommendations = recommendations
                    db_asset.location = location
                    db_asset.status = status
                    db_asset.date_of_purchase = str(date_of_purchase)
                    db_asset.cost = cost
                    db_asset.supplier = supplier
                    db_asset.gpo_no = gpo_no
                    db_asset.warranty_period = warranty_period
                    db_asset.quantity = quantity
                    db_asset.storage_type = storage_type
                    db.commit()
                    db.close()
                    st.success("Asset updated!")

                if delete:
                    db = SessionLocal()
                    db.query(Asset).filter(Asset.id == row_id).delete()
                    db.commit()
                    db.close()
                    st.warning("Asset deleted.")

