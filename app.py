import streamlit as st

# Define a function to display the menu and collect selections, now including prices and images
def show_menu(menu):
    selections = {}
    total_price = 0
    for category, items in menu.items():
        st.subheader(category)
        for item in items:
            col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
            with col1:
                st.image(item['image'], width=100)  # Display placeholder image
            with col2:
                is_selected = st.checkbox(item['name'], key=item['name'])
                st.caption(f"${item['price']}")  # Display item price
            with col3:
                if is_selected:
                    # Dropdown for modifications
                    modification = st.selectbox(f"Customize your {item['name']}:", item['modifications'], format_func=lambda x: x['name'], key=f"mod_{item['name']}")
                    selected_mod_price = modification['price']
                    selections[item['name']] = {'modification': modification['name'], 'total_price': item['price'] + selected_mod_price}
                    total_price += selections[item['name']]['total_price']
            with col4:
                if is_selected:
                    # Show price adjustment for selected modification, if any
                    st.caption(f"+${selected_mod_price}")
    return selections, total_price

# Define a function to display order summary, now with total price calculation
def order_summary(selections, total_price):
    st.subheader("Order Summary")
    if selections:
        for item, details in selections.items():
            st.write(f"{item}: {details['modification']} - ${details['total_price']}")
        st.markdown(f"**Total Order Price: ${total_price}**")
    else:
        st.write("You have not selected any items.")

# Sample menu data with prices and placeholder images
menu_data = {
    'Appetizers': [
        {'name': 'Spring Rolls', 'price': 5, 'modifications': [{'name': 'Extra Spicy', 'price': 1}, {'name': 'Gluten-Free', 'price': 2}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
        {'name': 'Garlic Bread', 'price': 4, 'modifications': [{'name': 'Extra Garlic', 'price': 0.5}, {'name': 'No Cheese', 'price': 0}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
    ],
    'Main Course': [
        {'name': 'Grilled Salmon', 'price': 15, 'modifications': [{'name': 'Well Done', 'price': 0}, {'name': 'Medium Rare', 'price': 0}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
        {'name': 'Vegetarian Pizza', 'price': 12, 'modifications': [{'name': 'Extra Cheese', 'price': 2}, {'name': 'Vegan Cheese', 'price': 2.5}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
    ],
    'Desserts': [
        {'name': 'Cheesecake', 'price': 6, 'modifications': [{'name': 'Strawberry Topping', 'price': 1.5}, {'name': 'Chocolate Topping', 'price': 1.5}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
        {'name': 'Ice Cream Sundae', 'price': 5, 'modifications': [{'name': 'Extra Nuts', 'price': 0.75}, {'name': 'No Nuts', 'price': 0}, {'name': 'None', 'price': 0}], 'image': 'https://via.placeholder.com/100'},
    ]
}

# Initialize session state to keep track of the progress and total price
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.total_price = 0

# Title for the ordering UI
st.title("DoorDash Restaurant Ordering System")

# Progress bar
progress_bar = st.progress(0)

# Step 1: Show menu and collect selections with prices
if st.session_state.step == 1:
    st.session_state.selections, st.session_state.total_price = show_menu(menu_data)
    progress_bar.progress(33)
    if st.button("Next"):
        st.session_state.step = 2

# Step 2: Show order summary and confirm order
elif st.session_state.step == 2:
    order_summary(st.session_state.selections, st.session_state.total_price)
    progress_bar.progress(66)
    if st.button("Confirm Order"):
        st.session_state.step = 3

# Step 3: Order confirmation
elif st.session_state.step == 3:
    st.subheader("Thank you for your order!")
    st.write("Your order has been placed successfully.")
    st.markdown(f"**Total Charged: ${st.session_state.total_price}**")
    progress_bar.progress(100)
